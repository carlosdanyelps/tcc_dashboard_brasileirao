import { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Tooltip,
} from "chart.js";
import type { ChartData } from "chart.js";
import "./ResultadosTemporada.css";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

interface ResultadosTemporadaProps {
  anoSelecionado: number;
}

interface TeamSeason {
  time: string;
  vitorias: number;
  empates: number;
  derrotas: number;
  pontos: number;
}

const ResultadosTemporada = ({ anoSelecionado }: ResultadosTemporadaProps) => {
  const [data, setData] = useState<ChartData<"bar", number[], string> | null>(null);

  useEffect(() => {
    let active = true;

    fetch(`http://127.0.0.1:5000/tabela?ano=${anoSelecionado}`)
      .then((response) => response.json() as Promise<TeamSeason[]>)
      .then((teams) => {
        if (!active) return;
        const topTeams = teams.slice(0, 8);
        setData({
          labels: topTeams.map((team) => team.time),
          datasets: [
            {
              label: "Vitórias",
              data: topTeams.map((team) => team.vitorias),
              backgroundColor: "rgba(24, 119, 82, 0.82)",
              borderRadius: 3,
            },
            {
              label: "Empates",
              data: topTeams.map((team) => team.empates),
              backgroundColor: "rgba(226, 166, 52, 0.82)",
              borderRadius: 3,
            },
            {
              label: "Derrotas",
              data: topTeams.map((team) => team.derrotas),
              backgroundColor: "rgba(214, 80, 57, 0.72)",
              borderRadius: 3,
            },
          ],
        });
      })
      .catch((error) => console.error("Erro ao carregar resultados:", error));

    return () => {
      active = false;
    };
  }, [anoSelecionado]);

  return (
    <section className="season-chart">
      <header className="season-chart-header">
        <h2>Perfil de resultados</h2>
        <p>Campanha dos oito primeiros em {anoSelecionado}</p>
      </header>
      {data ? (
        <Bar
          data={data}
          options={{
            responsive: true,
            maintainAspectRatio: false,
            scales: { x: { stacked: true }, y: { stacked: true, beginAtZero: true } },
            plugins: { legend: { position: "bottom" as const } },
          }}
        />
      ) : (
        <p className="season-chart-loading">Carregando...</p>
      )}
    </section>
  );
};

export default ResultadosTemporada;
