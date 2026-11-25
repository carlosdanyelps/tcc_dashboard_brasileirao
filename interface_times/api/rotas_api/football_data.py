import json
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[1] / ".env")

API_BASE_URL = "https://api.football-data.org/v4"
CACHE_TTL_SECONDS = 300
REQUEST_TIMEOUT_SECONDS = 15


class FootballDataError(Exception):
    def __init__(self, message, status_code=502):
        super().__init__(message)
        self.status_code = status_code


_cache = {"expires_at": 0.0, "data": None}
_cache_lock = threading.Lock()


def _request_json(path, token):
    request = Request(
        f"{API_BASE_URL}{path}",
        headers={
            "X-Auth-Token": token,
            "Accept": "application/json",
            "User-Agent": "BrasileiraoDashboard/1.0",
        },
    )
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        if error.code in (401, 403):
            raise FootballDataError(
                "A chave é inválida ou não tem acesso ao Brasileirão Série A.",
                status_code=error.code,
            ) from error
        if error.code == 429:
            raise FootballDataError(
                "Limite de consultas da football-data.org atingido. Tente novamente mais tarde.",
                status_code=429,
            ) from error
        raise FootballDataError(
            f"A football-data.org respondeu com erro HTTP {error.code}.",
            status_code=502,
        ) from error
    except (URLError, TimeoutError) as error:
        raise FootballDataError(
            "Não foi possível conectar à football-data.org.",
            status_code=502,
        ) from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise FootballDataError(
            "A football-data.org retornou uma resposta inválida.",
            status_code=502,
        ) from error


def _team_data(team):
    return {
        "id": team.get("id"),
        "name": team.get("name", ""),
        "short_name": team.get("shortName") or team.get("tla") or team.get("name", ""),
        "crest": team.get("crest"),
    }


def _normalize_match(match):
    full_time = match.get("score", {}).get("fullTime", {})
    return {
        "id": match.get("id"),
        "utc_date": match.get("utcDate"),
        "status": match.get("status", "SCHEDULED"),
        "matchday": match.get("matchday"),
        "home_team": _team_data(match.get("homeTeam", {})),
        "away_team": _team_data(match.get("awayTeam", {})),
        "home_score": full_time.get("home"),
        "away_score": full_time.get("away"),
    }


def _normalize_standing(row):
    return {
        "position": row.get("position"),
        "team": _team_data(row.get("team", {})),
        "played": row.get("playedGames", 0),
        "won": row.get("won", 0),
        "draw": row.get("draw", 0),
        "lost": row.get("lost", 0),
        "points": row.get("points", 0),
        "goals_for": row.get("goalsFor", 0),
        "goals_against": row.get("goalsAgainst", 0),
        "goal_difference": row.get("goalDifference", 0),
    }


def get_current_season_data():
    token = os.getenv("FOOTBALL_DATA_API_KEY", "").strip()
    if not token:
        load_dotenv(Path(__file__).resolve().parents[1] / ".env")
        token = os.getenv("FOOTBALL_DATA_API_KEY", "").strip()
    if not token:
        raise FootballDataError(
            "Configure FOOTBALL_DATA_API_KEY em interface_times/api/.env para habilitar os dados atuais.",
            status_code=503,
        )

    now = time.monotonic()
    if _cache["data"] is not None and now < _cache["expires_at"]:
        return _cache["data"]

    with _cache_lock:
        now = time.monotonic()
        if _cache["data"] is not None and now < _cache["expires_at"]:
            return _cache["data"]

        matches_response = _request_json("/competitions/BSA/matches", token)
        standings_response = _request_json("/competitions/BSA/standings", token)

        competition = matches_response.get("competition", {})
        matches = matches_response.get("matches", [])
        current_season = (
            competition.get("currentSeason")
            or (matches[0].get("season") if matches else None)
            or {}
        )
        standings = standings_response.get("standings", [])
        total_standing = next(
            (item for item in standings if item.get("type") == "TOTAL"),
            standings[0] if standings else {},
        )
        start_date = current_season.get("startDate") or ""
        normalized = {
            "competition": competition.get("name", "Campeonato Brasileiro Série A"),
            "season": start_date[:4] or current_season.get("year"),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "refresh_interval_seconds": CACHE_TTL_SECONDS,
            "matches": [_normalize_match(match) for match in matches],
            "standings": [
                _normalize_standing(row)
                for row in total_standing.get("table", [])
            ],
        }
        _cache["data"] = normalized
        _cache["expires_at"] = time.monotonic() + CACHE_TTL_SECONDS
        return normalized


def clear_cache():
    with _cache_lock:
        _cache["data"] = None
        _cache["expires_at"] = 0.0
