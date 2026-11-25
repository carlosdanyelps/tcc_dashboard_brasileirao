import { useEffect, useMemo, useState, type CSSProperties } from "react";
import Header from "../../Components/Header/Header";
import "./style.css";

interface TeamSummary {
  ID: number | null;
  "URL escudo": string | null;
  cor: string;
  bordaCor: string;
}

interface TeamOptions {
  times: string[];
  temporadas: number[];
}

interface MatchResult {
  temporada: number;
  data: string;
  rodada: number | null;
  mandante: string;
  visitante: string;
  gols_mandante: number;
  gols_visitante: number;
  vencedor: string | null;
}

interface HeadToHeadData {
  time1: string;
  time2: string;
  temporada: number | null;
  temporadas_disponiveis: number[];
  resumo: {
    partidas: number;
    vitorias_time1: number;
    vitorias_time2: number;
    empates: number;
    gols_time1: number;
    gols_time2: number;
    total_gols: number;
    media_gols: number;
  };
  partidas_detalhadas: MatchResult[];
}

const API_URL = "http://127.0.0.1:5000";

const initials = (team: string) =>
  team
    .split(/[\s-]+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0])
    .join("")
    .toUpperCase();

const displayDate = (date: string) => {
  const parsedDate = new Date(`${date}T12:00:00`);
  return Number.isNaN(parsedDate.getTime())
    ? date
    : parsedDate.toLocaleDateString("pt-BR");
};

const getTeamStyle = (
  summary: TeamSummary | undefined,
  fallback: { color: string; border: string },
): CSSProperties =>
  ({
    "--team-color": summary?.cor ?? fallback.color,
    "--team-border": summary?.bordaCor ?? fallback.border,
  }) as CSSProperties;

const TeamBadge = ({
  team,
  summary,
  fallback,
}: {
  team: string;
  summary: TeamSummary | undefined;
  fallback: { color: string; border: string };
}) => {
  const [imageFailed, setImageFailed] = useState(false);
  const crestUrl = summary?.["URL escudo"];

  useEffect(() => {
    setImageFailed(false);
  }, [crestUrl]);

  return (
    <div className="team-mark" style={getTeamStyle(summary, fallback)}>
      {crestUrl && !imageFailed ? (
        <img
          src={crestUrl}
          alt={`Escudo do ${team}`}
          onError={() => setImageFailed(true)}
        />
      ) : (
        <span aria-hidden="true">{initials(team)}</span>
      )}
    </div>
  );
};

const HeadToHead = () => {
  const [options, setOptions] = useState<TeamOptions | null>(null);
  const [team1, setTeam1] = useState("");
  const [team2, setTeam2] = useState("");
  const [season, setSeason] = useState("all");
  const [data, setData] = useState<HeadToHeadData | null>(null);
  const [teamSummaries, setTeamSummaries] = useState<Record<string, TeamSummary>>({});
  const [loadingOptions, setLoadingOptions] = useState(true);
  const [loading, setLoading] = useState(false);
  const [historyExpanded, setHistoryExpanded] = useState(false);
  const [error, setError] = useState("");
  const [optionsError, setOptionsError] = useState("");
  const [teamsError, setTeamsError] = useState("");

  useEffect(() => {
    let active = true;

    fetch(`${API_URL}/confronto-direto/opcoes`)
      .then(async (response) => {
        if (!response.ok) {
          throw new Error("Não foi possível carregar os clubes.");
        }
        return (await response.json()) as TeamOptions;
      })
      .then((result) => {
        if (!active) return;
        setOptions(result);
        const preferredTeam1 = result.times.find((team) => team === "Corinthians");
        const preferredTeam2 = result.times.find(
          (team) => team.includes("Atl") && team.endsWith("-MG"),
        );
        setTeam1(preferredTeam1 ?? result.times[0] ?? "");
        setTeam2(
          preferredTeam2 ??
            result.times.find((team) => team !== (preferredTeam1 ?? result.times[0])) ??
            "",
        );
      })
      .catch((fetchError: unknown) => {
        if (!active) return;
        setOptionsError(
          fetchError instanceof Error
            ? fetchError.message
            : "Erro inesperado ao carregar os clubes.",
        );
      })
      .finally(() => {
        if (active) setLoadingOptions(false);
      });

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    if (!team1 || !team2) return;

    let active = true;
    const fetchTeamSummary = async (team: string) => {
      const params = new URLSearchParams({ time: team });
      const response = await fetch(`${API_URL}/timemain/time_main?${params.toString()}`);
      if (!response.ok) {
        throw new Error(`Não foi possível carregar o escudo e as cores de ${team}.`);
      }
      return (await response.json()) as TeamSummary;
    };

    setTeamsError("");

    Promise.all([fetchTeamSummary(team1), fetchTeamSummary(team2)])
      .then(([summary1, summary2]) => {
        if (!active) return;
        setTeamSummaries((current) => ({
          ...current,
          [team1]: summary1,
          [team2]: summary2,
        }));
      })
      .catch((fetchError: unknown) => {
        if (!active) return;
        setTeamsError(
          fetchError instanceof Error
            ? fetchError.message
            : "Erro inesperado ao carregar os escudos e as cores.",
        );
      });

    return () => {
      active = false;
    };
  }, [team1, team2]);

  useEffect(() => {
    if (!team1 || !team2 || team1 === team2) {
      setData(null);
      return;
    }

    let active = true;
    const params = new URLSearchParams({ time1: team1, time2: team2 });
    if (season !== "all") params.set("temporada", season);

    setLoading(true);
    setError("");

    fetch(`${API_URL}/confronto-direto?${params.toString()}`)
      .then(async (response) => {
        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.erro ?? "Não foi possível carregar o confronto.");
        }
        return result as HeadToHeadData;
      })
      .then((result) => {
        if (active) setData(result);
      })
      .catch((fetchError: unknown) => {
        if (!active) return;
        setError(
          fetchError instanceof Error
            ? fetchError.message
            : "Erro inesperado ao carregar o confronto.",
        );
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, [season, team1, team2]);

  useEffect(() => {
    setHistoryExpanded(false);
  }, [season, team1, team2]);

  const winTotal =
    (data?.resumo.vitorias_time1 ?? 0) +
    (data?.resumo.vitorias_time2 ?? 0);
  const win1Share = winTotal
    ? ((data?.resumo.vitorias_time1 ?? 0) / winTotal) * 100
    : 0;
  const win2Share = winTotal ? 100 - win1Share : 0;
  const goalTotal = data?.resumo.total_gols ?? 0;
  const goal1Share = goalTotal
    ? ((data?.resumo.gols_time1 ?? 0) / goalTotal) * 100
    : 0;
  const goal2Share = goalTotal ? 100 - goal1Share : 0;

  const matchYears = useMemo(
    () => new Set(data?.temporadas_disponiveis ?? []),
    [data],
  );

  const availableSeasons = options?.temporadas ?? [];
  const summary1 = teamSummaries[team1];
  const summary2 = teamSummaries[team2];
  const teamColors: Record<string, string> = {
    [team1]: summary1?.bordaCor ?? "#1c6248",
    [team2]: summary2?.bordaCor ?? "#73847a",
  };
  const visibleMatches = historyExpanded
    ? data?.partidas_detalhadas ?? []
    : data?.partidas_detalhadas.slice(0, 5) ?? [];
  const remainingMatches = Math.max(
    0,
    (data?.partidas_detalhadas.length ?? 0) - visibleMatches.length,
  );

  return (
    <main className="head-to-head-page">
      <Header />
      <div className="head-to-head-content">
        <section className="head-to-head-heading">
          <div>
            <span className="head-to-head-eyebrow">Brasileirão • retrospecto completo</span>
            <h1>Confronto direto</h1>
            <p>
              Compare a história de dois clubes, temporada por temporada, e
              relembre cada placar.
            </p>
          </div>
          <label className="head-season-filter">
            <span>Recorte de temporada</span>
            <select
              value={season}
              onChange={(event) => setSeason(event.target.value)}
              disabled={loadingOptions || !options}
            >
              <option value="all">Todas as temporadas</option>
              {availableSeasons.map((year) => (
                <option key={year} value={year}>
                  {year}
                  {matchYears.has(year) ? "" : " • sem confronto"}
                </option>
              ))}
            </select>
          </label>
        </section>

        <section className="head-team-picker" aria-label="Times do confronto">
          <label className="head-team-select">
            <span>Time 1</span>
            <select
              value={team1}
              onChange={(event) => setTeam1(event.target.value)}
              disabled={loadingOptions || !options}
            >
              {options?.times.map((team) => (
                <option key={team} value={team} disabled={team === team2}>
                  {team}
                </option>
              ))}
            </select>
          </label>
          <button
            type="button"
            className="swap-teams"
            aria-label="Inverter os times"
            title="Inverter os times"
            onClick={() => {
              setTeam1(team2);
              setTeam2(team1);
            }}
            disabled={!team1 || !team2}
          >
            ⇄
          </button>
          <label className="head-team-select">
            <span>Time 2</span>
            <select
              value={team2}
              onChange={(event) => setTeam2(event.target.value)}
              disabled={loadingOptions || !options}
            >
              {options?.times.map((team) => (
                <option key={team} value={team} disabled={team === team1}>
                  {team}
                </option>
              ))}
            </select>
          </label>
        </section>

        {(optionsError || error || teamsError) && (
          <p className="head-to-head-error" role="alert">
            {optionsError || teamsError || error}
          </p>
        )}

        <section className="rivalry-panel">
          <div className="rivalry-title-row">
            <span>Histórico de confrontos</span>
            <span className="rivalry-period">
              {season === "all" ? "Todas as temporadas" : `Temporada ${season}`}
            </span>
          </div>

          <div className="rivalry-scoreboard">
            <div className="rivalry-team">
              <TeamBadge
                team={team1}
                summary={summary1}
                fallback={{ color: "rgba(113, 92, 6, 0.6)", border: "#dfc243" }}
              />
              <strong>{team1 || "Selecione um time"}</strong>
              <span>{data?.resumo.vitorias_time1 ?? 0} vitórias</span>
            </div>

            <div className="rivalry-center">
              <div className="match-count">
                <strong>
                  {loading ? "…" : data?.resumo.partidas.toLocaleString("pt-BR") ?? "—"}
                </strong>
                <span>PARTIDAS DISPUTADAS</span>
              </div>
              <div
                className="wins-bar"
                role="img"
                aria-label={`${team1}: ${data?.resumo.vitorias_time1 ?? 0} vitórias; ${team2}: ${data?.resumo.vitorias_time2 ?? 0} vitórias`}
              >
                <span style={{ width: `${win1Share}%`, backgroundColor: summary1?.cor }} />
                <span style={{ width: `${win2Share}%`, backgroundColor: summary2?.cor }} />
              </div>
              <div className="wins-numbers">
                <strong style={{ color: summary1?.bordaCor }}>{data?.resumo.vitorias_time1 ?? 0}</strong>
                <span>{data?.resumo.empates ?? 0} EMPATES</span>
                <strong style={{ color: summary2?.bordaCor }}>{data?.resumo.vitorias_time2 ?? 0}</strong>
              </div>
              <div className="wins-captions">
                <span style={{ color: summary1?.bordaCor }}>VITÓRIAS DO {team1}</span>
                <span style={{ color: summary2?.bordaCor }}>VITÓRIAS DO {team2}</span>
              </div>
            </div>

            <div className="rivalry-team">
              <TeamBadge
                team={team2}
                summary={summary2}
                fallback={{ color: "rgba(38, 67, 51, 0.6)", border: "#789082" }}
              />
              <strong>{team2 || "Selecione um time"}</strong>
              <span>{data?.resumo.vitorias_time2 ?? 0} vitórias</span>
            </div>
          </div>

          <div className="goals-summary">
            <div className="goals-title">
              <span>{data?.resumo.total_gols.toLocaleString("pt-BR") ?? 0} GOLS NO CONFRONTO</span>
            </div>
            <div
              className="goals-bar"
              role="img"
              aria-label={`${team1}: ${data?.resumo.gols_time1 ?? 0} gols; ${team2}: ${data?.resumo.gols_time2 ?? 0} gols`}
            >
              <span style={{ width: `${goal1Share}%`, backgroundColor: summary1?.cor }} />
              <span style={{ width: `${goal2Share}%`, backgroundColor: summary2?.cor }} />
            </div>
            <div className="goals-numbers">
              <strong style={{ color: summary1?.bordaCor }}>{data?.resumo.gols_time1 ?? 0}</strong>
              <span>
                MÉDIA DE {data?.resumo.media_gols.toLocaleString("pt-BR") ?? "0,00"} GOLS POR PARTIDA
              </span>
              <strong style={{ color: summary2?.bordaCor }}>{data?.resumo.gols_time2 ?? 0}</strong>
            </div>
            <div className="goals-captions">
              <span style={{ color: summary1?.bordaCor }}>GOLS DO {team1}</span>
              <span style={{ color: summary2?.bordaCor }}>GOLS DO {team2}</span>
            </div>
          </div>
        </section>

        <section className="match-history">
          <header className="match-history-header">
            <div>
              <span className="head-to-head-eyebrow">Placar a placar</span>
              <h2>Histórico de partidas</h2>
            </div>
            <div className="match-history-actions">
              <span>{data?.partidas_detalhadas.length ?? 0} jogos</span>
              {data && data.partidas_detalhadas.length > 5 && (
                <button
                  type="button"
                  className="match-history-toggle"
                  aria-expanded={historyExpanded}
                  onClick={() => setHistoryExpanded((expanded) => !expanded)}
                >
                  {historyExpanded ? "Mostrar menos" : "Ver todos"}
                  <span className={historyExpanded ? "expanded" : ""} aria-hidden="true">
                    ⌄
                  </span>
                </button>
              )}
            </div>
          </header>

          {loadingOptions || loading ? (
            <p className="match-history-empty">Carregando confrontos...</p>
          ) : visibleMatches.length ? (
            <div className="match-table-wrap">
              {!historyExpanded && remainingMatches > 0 && (
                <p className="match-history-note">
                  Exibindo os 5 confrontos mais recentes de {data?.partidas_detalhadas.length} partidas.
                </p>
              )}
              <table className="match-table">
                <thead>
                  <tr>
                    <th>Temporada</th>
                    <th>Data / rodada</th>
                    <th>Mandante</th>
                    <th>Placar</th>
                    <th>Visitante</th>
                  </tr>
                </thead>
                <tbody>
                  {visibleMatches.map((match) => (
                    <tr
                      key={`${match.temporada}-${match.data}-${match.rodada}-${match.mandante}-${match.visitante}`}
                    >
                      <td>{match.temporada}</td>
                      <td>
                        {displayDate(match.data)}
                        {match.rodada ? ` • ${match.rodada}ª rodada` : ""}
                      </td>
                      <td
                        className={match.vencedor === match.mandante ? "match-winner" : ""}
                        style={match.vencedor === match.mandante
                          ? { color: teamColors[match.mandante] }
                          : undefined}
                      >
                        {match.mandante}
                      </td>
                      <td className="match-score">
                        {match.gols_mandante} <span>—</span> {match.gols_visitante}
                      </td>
                      <td
                        className={match.vencedor === match.visitante ? "match-winner" : ""}
                        style={match.vencedor === match.visitante
                          ? { color: teamColors[match.visitante] }
                          : undefined}
                      >
                        {match.visitante}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="match-history-empty">
              {error
                ? "Não foi possível carregar o histórico."
                : "Não há confrontos entre esses times neste recorte de temporadas."}
            </p>
          )}
        </section>
      </div>
    </main>
  );
};

export default HeadToHead;
