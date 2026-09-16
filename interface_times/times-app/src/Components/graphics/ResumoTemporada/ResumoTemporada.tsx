import { useEffect, useState } from "react";
import "./ResumoTemporada.css";

interface ResumoTemporadaProps {
  anoSelecionado: number;
}

interface TeamSeason {
  time: string;
  pontos: number;
  gols_pro: number;
  gols_tomados: number;
  vitorias: number;
}

const ResumoTemporada = ({ anoSelecionado }: ResumoTemporadaProps) => {
  const [teams, setTeams] = useState<TeamSeason[]>([]);

  useEffect(() => {
    let active = true;

    fetch(`http://127.0.0.1:5000/tabela?ano=${anoSelecionado}`)
      .then((response) => response.json() as Promise<TeamSeason[]>)
      .then((data) => {
        if (active && Array.isArray(data)) setTeams(data);
      })
      .catch((error) => console.error("Erro ao carregar resumo:", error));

    return () => {
      active = false;
    };
  }, [anoSelecionado]);

  const champion = teams[0];
  const totalGoals = teams.reduce((total, team) => total + team.gols_pro, 0);
  const averagePoints = teams.length
    ? (teams.reduce((total, team) => total + team.pontos, 0) / teams.length).toFixed(1)
    : "-";
  const topScorer = [...teams].sort((a, b) => b.gols_pro - a.gols_pro)[0];

  return (
    <section className="season-summary" aria-label={`Resumo da temporada ${anoSelecionado}`}>
      <div className="summary-intro">
        <span className="summary-kicker">Painel da temporada</span>
        <strong>{anoSelecionado}</strong>
        <span>{teams.length ? `${teams.length} clubes na disputa` : "Carregando dados"}</span>
      </div>
      <div className="summary-metrics">
        <div className="summary-metric">
          <span>Campeão</span>
          <strong>{champion?.time ?? "-"}</strong>
          <small>{champion ? `${champion.pontos} pontos` : "Aguardando API"}</small>
        </div>
        <div className="summary-metric">
          <span>Gols no campeonato</span>
          <strong>{totalGoals || "-"}</strong>
          <small>{topScorer ? `${topScorer.time} lidera com ${topScorer.gols_pro}` : ""}</small>
        </div>
        <div className="summary-metric">
          <span>Média de pontos</span>
          <strong>{averagePoints}</strong>
          <small>por clube</small>
        </div>
      </div>
    </section>
  );
};

export default ResumoTemporada;
