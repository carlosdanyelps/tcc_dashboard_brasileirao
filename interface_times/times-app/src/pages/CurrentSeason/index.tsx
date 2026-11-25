import { useEffect, useMemo, useState } from "react";
import Header from "../../Components/Header/Header";
import "./style.css";

interface Team {
  id: number | null;
  name: string;
  short_name: string;
  crest: string | null;
}

interface Match {
  id: number;
  utc_date: string;
  status: string;
  matchday: number | null;
  home_team: Team;
  away_team: Team;
  home_score: number | null;
  away_score: number | null;
}

interface Standing {
  position: number;
  team: Team;
  played: number;
  won: number;
  draw: number;
  lost: number;
  points: number;
  goals_for: number;
  goals_against: number;
  goal_difference: number;
}

interface CurrentSeasonData {
  competition: string;
  season: string | number | null;
  updated_at: string;
  refresh_interval_seconds: number;
  matches: Match[];
  standings: Standing[];
}

const API_URL = "http://127.0.0.1:5000";
const REFRESH_INTERVAL_MS = 5 * 60 * 1000;

const statusLabels: Record<string, string> = {
  SCHEDULED: "Agendada",
  TIMED: "Agendada",
  IN_PLAY: "Em andamento",
  PAUSED: "Intervalo",
  FINISHED: "Encerrada",
  POSTPONED: "Adiada",
  SUSPENDED: "Suspensa",
  CANCELED: "Cancelada",
};

const formatDate = (date: string) =>
  new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(new Date(date));

const TeamCrest = ({ team }: { team: Team }) => {
  const [failed, setFailed] = useState(false);

  useEffect(() => setFailed(false), [team.crest]);

  return team.crest && !failed ? (
    <img
      className="current-team-crest"
      src={team.crest}
      alt=""
      loading="lazy"
      onError={() => setFailed(true)}
    />
  ) : (
    <span className="current-team-crest-fallback" aria-hidden="true">
      {team.short_name.slice(0, 3).toUpperCase()}
    </span>
  );
};

const MatchCard = ({ match }: { match: Match }) => {
  const hasScore = match.home_score !== null && match.away_score !== null;

  return (
    <article className="current-match-card">
      <header className="current-match-meta">
        <time dateTime={match.utc_date}>{formatDate(match.utc_date)}</time>
        <span>
          {match.matchday ? `${match.matchday}ª rodada · ` : ""}
          {statusLabels[match.status] ?? match.status}
        </span>
      </header>
      <div className="current-match-teams">
        <div className="current-match-team">
          <TeamCrest team={match.home_team} />
          <span>{match.home_team.name}</span>
        </div>
        <strong className="current-match-score" aria-label="Placar">
          {hasScore ? `${match.home_score} – ${match.away_score}` : "vs"}
        </strong>
        <div className="current-match-team">
          <TeamCrest team={match.away_team} />
          <span>{match.away_team.name}</span>
        </div>
      </div>
    </article>
  );
};

const CurrentSeason = () => {
  const [data, setData] = useState<CurrentSeasonData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;

    const fetchSeason = async () => {
      try {
        const response = await fetch(`${API_URL}/football-data/brasileirao`);
        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.erro ?? "Não foi possível carregar os dados atuais.");
        }
        if (active) {
          setData(result as CurrentSeasonData);
          setError("");
        }
      } catch (fetchError: unknown) {
        if (active) {
          setError(
            fetchError instanceof Error
              ? fetchError.message
              : "Erro inesperado ao carregar a temporada atual.",
          );
        }
      } finally {
        if (active) setLoading(false);
      }
    };

    void fetchSeason();
    const intervalId = window.setInterval(() => void fetchSeason(), REFRESH_INTERVAL_MS);

    return () => {
      active = false;
      window.clearInterval(intervalId);
    };
  }, []);

  const { liveMatches, upcomingMatches, recentMatches } = useMemo(() => {
    const allMatches = data?.matches ?? [];
    const now = Date.now();
    const chronological = [...allMatches].sort(
      (first, second) =>
        new Date(first.utc_date).getTime() - new Date(second.utc_date).getTime(),
    );
    const live = chronological.filter((match) =>
      ["IN_PLAY", "PAUSED"].includes(match.status),
    );
    const upcoming = chronological
      .filter(
        (match) =>
          ["SCHEDULED", "TIMED"].includes(match.status) &&
          new Date(match.utc_date).getTime() >= now,
      )
      .slice(0, 8);
    const recent = chronological
      .filter((match) => match.status === "FINISHED")
      .reverse()
      .slice(0, 8);
    return { liveMatches: live, upcomingMatches: upcoming, recentMatches: recent };
  }, [data]);

  return (
    <div className="current-season-page">
      <Header />
      <main className="current-season-content">
        <header className="current-season-hero">
          <div>
            <p className="current-season-eyebrow">football-data.org · Série A</p>
            <h1>Brasileirão atual</h1>
            <p>Partidas da temporada, resultados e classificação.</p>
          </div>
          {data && (
            <p className="current-season-year">
              Temporada <strong>{data.season ?? "atual"}</strong>
            </p>
          )}
        </header>

        {error && (
          <p className="current-season-error" role="alert">
            {error}
          </p>
        )}

        {loading && <p className="current-season-message">Carregando temporada...</p>}

        {!loading && !error && data && (
          <>
            <section className="current-matches-section" aria-labelledby="live-heading">
              <header className="current-section-heading">
                <h2 id="live-heading">Ao vivo</h2>
                <span>{liveMatches.length} partidas</span>
              </header>
              {liveMatches.length ? (
                <div className="current-match-list">
                  {liveMatches.map((match) => <MatchCard key={match.id} match={match} />)}
                </div>
              ) : (
                <p className="current-season-message">Nenhuma partida em andamento.</p>
              )}
            </section>

            <section className="current-matches-section" aria-labelledby="upcoming-heading">
              <header className="current-section-heading">
                <h2 id="upcoming-heading">Próximos jogos</h2>
              </header>
              {upcomingMatches.length ? (
                <div className="current-match-list">
                  {upcomingMatches.map((match) => <MatchCard key={match.id} match={match} />)}
                </div>
              ) : (
                <p className="current-season-message">Não há próximos jogos disponíveis.</p>
              )}
            </section>

            <section className="current-matches-section" aria-labelledby="recent-heading">
              <header className="current-section-heading">
                <h2 id="recent-heading">Últimos resultados</h2>
              </header>
              {recentMatches.length ? (
                <div className="current-match-list">
                  {recentMatches.map((match) => <MatchCard key={match.id} match={match} />)}
                </div>
              ) : (
                <p className="current-season-message">Ainda não há resultados finalizados.</p>
              )}
            </section>

            <section className="current-standings-section" aria-labelledby="standings-heading">
              <header className="current-section-heading">
                <h2 id="standings-heading">Classificação</h2>
              </header>
              {data.standings.length ? (
                <div className="current-standings-wrap">
                  <table className="current-standings-table">
                    <caption className="visually-hidden">
                      Classificação da temporada {data.season ?? "atual"} do Brasileirão Série A
                    </caption>
                    <thead>
                      <tr>
                        <th scope="col">Pos.</th>
                        <th scope="col">Clube</th>
                        <th scope="col">Pts</th>
                        <th scope="col">PJ</th>
                        <th scope="col">V</th>
                        <th scope="col">E</th>
                        <th scope="col">D</th>
                        <th scope="col">SG</th>
                      </tr>
                    </thead>
                    <tbody>
                      {data.standings.map((row) => (
                        <tr key={row.team.id ?? row.team.name}>
                          <td>{row.position}</td>
                          <th scope="row">
                            <span className="current-standing-team">
                              <TeamCrest team={row.team} />
                              {row.team.name}
                            </span>
                          </th>
                          <td><strong>{row.points}</strong></td>
                          <td>{row.played}</td>
                          <td>{row.won}</td>
                          <td>{row.draw}</td>
                          <td>{row.lost}</td>
                          <td>{row.goal_difference}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p className="current-season-message">
                  A classificação ainda não está disponível para esta temporada.
                </p>
              )}
            </section>

            <footer className="current-season-footer">
              Última consulta ao provedor: {formatDate(data.updated_at)}
            </footer>
          </>
        )}
      </main>
    </div>
  );
};

export default CurrentSeason;
