import { useEffect, useMemo, useState } from "react";
import Header from "../../Components/Header/Header";
import "./style.css";

type CoachMetric = "vitorias" | "derrotas" | "empates" | "partidas";

interface PlayerRanking {
  jogador: string;
  clubes: string[];
  gols: number;
}

interface CoachRanking {
  tecnico: string;
  clubes: string[];
  vitorias: number;
  derrotas: number;
  empates: number;
  partidas: number;
  aproveitamento: number;
}

interface IndividualDashboardData {
  temporada: number | null;
  temporadas_disponiveis: number[];
  resumo: {
    partidas: number;
    partidas_com_tecnico: number;
    partidas_com_ambos_tecnicos: number;
    gols_creditados: number;
    jogadores: number;
    tecnicos: number;
  };
  artilheiros: PlayerRanking[];
  tecnicos: CoachRanking[];
}

const metricLabels: Record<CoachMetric, string> = {
  vitorias: "Vitórias",
  derrotas: "Derrotas",
  empates: "Empates",
  partidas: "Partidas",
};

const PlayersCoaches = () => {
  const [season, setSeason] = useState("all");
  const [data, setData] = useState<IndividualDashboardData | null>(null);
  const [seasons, setSeasons] = useState<number[]>([]);
  const [coachMetric, setCoachMetric] = useState<CoachMetric>("vitorias");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    const query = season === "all" ? "" : `?temporada=${season}`;

    setLoading(true);
    setError("");

    fetch(`http://127.0.0.1:5000/jogadores-tecnicos${query}`)
      .then(async (response) => {
        if (!response.ok) {
          throw new Error("Não foi possível carregar as estatísticas individuais.");
        }
        return (await response.json()) as IndividualDashboardData;
      })
      .then((result) => {
        if (!active) return;
        setData(result);
        setSeasons(result.temporadas_disponiveis);
      })
      .catch((fetchError: unknown) => {
        if (!active) return;
        setError(
          fetchError instanceof Error
            ? fetchError.message
            : "Erro inesperado ao carregar as estatísticas.",
        );
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, [season]);

  const rankedCoaches = useMemo(() => {
    if (!data) return [];
    return [...data.tecnicos]
      .sort((a, b) => {
        const difference = b[coachMetric] - a[coachMetric];
        return difference || b.partidas - a.partidas || a.tecnico.localeCompare(b.tecnico);
      })
      .slice(0, 10);
  }, [coachMetric, data]);

  const topScorer = data?.artilheiros[0];
  const topCoach = [...(data?.tecnicos ?? [])].sort(
    (a, b) => b.vitorias - a.vitorias || b.partidas - a.partidas,
  )[0];

  return (
    <main className="people-page">
      <Header />
      <div className="people-content">
        <section className="people-hero">
          <div className="people-hero-copy">
            <span className="people-eyebrow">Brasileirão • dados individuais</span>
            <h1>Quem decide o jogo?</h1>
            <p>
              Artilheiros e técnicos em destaque, com rankings por temporada ou
              em todo o período disponível.
            </p>
          </div>
          <label className="season-filter">
            <span>Temporada</span>
            <select value={season} onChange={(event) => setSeason(event.target.value)}>
              <option value="all">Todas as temporadas</option>
              {seasons.map((year) => (
                <option key={year} value={year}>
                  {year}
                </option>
              ))}
            </select>
          </label>
        </section>

        <section className="people-metrics" aria-label="Resumo das estatísticas">
          <article className="people-metric people-metric-highlight">
            <span>Artilheiro do recorte</span>
            <strong>{topScorer?.jogador ?? "—"}</strong>
            <small>{topScorer ? `${topScorer.gols} gols` : "Aguardando dados"}</small>
          </article>
          <article className="people-metric">
            <span>Gols creditados</span>
            <strong>{data?.resumo.gols_creditados.toLocaleString("pt-BR") ?? "—"}</strong>
            <small>Gols com autoria registrada</small>
          </article>
          <article className="people-metric">
            <span>Técnico com mais vitórias</span>
            <strong>{topCoach?.tecnico ?? "—"}</strong>
            <small>{topCoach ? `${topCoach.vitorias} vitórias` : "Aguardando dados"}</small>
          </article>
          <article className="people-metric">
            <span>Partidas analisadas</span>
            <strong>{data?.resumo.partidas.toLocaleString("pt-BR") ?? "—"}</strong>
            <small>
              {data
                ? `${data.resumo.partidas_com_ambos_tecnicos.toLocaleString("pt-BR")} com ambos os técnicos`
                : "Aguardando dados"}
            </small>
          </article>
        </section>

        {error && <p className="people-message people-error">{error}</p>}

        <div className="people-rankings">
          <section className="ranking-panel scorer-panel">
            <header className="ranking-heading">
              <div>
                <span className="panel-kicker">Gols marcados</span>
                <h2>Artilheiros</h2>
                <p>Gols contra não entram nesta contagem.</p>
              </div>
              <span className="ranking-badge">{data?.resumo.jogadores ?? 0} jogadores</span>
            </header>

            {loading ? (
              <p className="people-message">Carregando artilharia...</p>
            ) : data?.artilheiros.length ? (
              <ol className="scorer-list">
                {data.artilheiros.map((player, index) => (
                  <li key={player.jogador}>
                    <span className="scorer-position">{String(index + 1).padStart(2, "0")}</span>
                    <div className="scorer-details">
                      <strong>{player.jogador}</strong>
                      <small>{player.clubes.join(" / ") || "Clube não informado"}</small>
                    </div>
                    <strong className="scorer-goals">
                      {player.gols} <span>GOLS</span>
                    </strong>
                  </li>
                ))}
              </ol>
            ) : (
              <p className="people-message">
                {error || "Não há gols com autoria registrada neste recorte."}
              </p>
            )}
          </section>

          <section className="ranking-panel coach-panel">
            <header className="ranking-heading coach-heading">
              <div>
                <span className="panel-kicker">Comando à beira do campo</span>
                <h2>Ranking de técnicos</h2>
                <p>Compare resultados e volume de partidas.</p>
              </div>
              <span className="ranking-badge">{data?.resumo.tecnicos ?? 0} técnicos</span>
            </header>

            <div className="coach-tabs" role="group" aria-label="Ordenar técnicos por">
              {(Object.keys(metricLabels) as CoachMetric[]).map((metric) => (
                <button
                  key={metric}
                  type="button"
                  className={coachMetric === metric ? "active" : ""}
                  aria-pressed={coachMetric === metric}
                  onClick={() => setCoachMetric(metric)}
                >
                  {metricLabels[metric]}
                </button>
              ))}
            </div>

            {loading ? (
              <p className="people-message">Carregando ranking...</p>
            ) : rankedCoaches.length ? (
              <div className="coach-table-wrap">
                <table className="coach-table">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Técnico</th>
                      <th>V</th>
                      <th>E</th>
                      <th>D</th>
                      <th>J</th>
                      <th>Aprov.</th>
                    </tr>
                  </thead>
                  <tbody>
                    {rankedCoaches.map((coach, index) => (
                      <tr key={coach.tecnico}>
                        <td className="coach-position">{String(index + 1).padStart(2, "0")}</td>
                        <td>
                          <strong>{coach.tecnico}</strong>
                          <small>{coach.clubes.join(", ")}</small>
                        </td>
                        <td>{coach.vitorias}</td>
                        <td>{coach.empates}</td>
                        <td>{coach.derrotas}</td>
                        <td>{coach.partidas}</td>
                        <td>{coach.aproveitamento.toLocaleString("pt-BR")}%</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="people-message">
                {error || "Não há registros de técnicos neste recorte."}
              </p>
            )}
          </section>
        </div>

        <p className="people-footnote">
          Dados individuais disponíveis de {seasons[0] ?? 2014} em diante. O ranking de técnicos
          considera apenas partidas com o nome do treinador registrado; aproveitamento
          segue a pontuação padrão (3 pontos por vitória e 1 por empate).
          {data && (
            <> Partidas com ao menos um técnico identificado: {data.resumo.partidas_com_tecnico.toLocaleString("pt-BR")}.</>
          )}
        </p>
      </div>
    </main>
  );
};

export default PlayersCoaches;
