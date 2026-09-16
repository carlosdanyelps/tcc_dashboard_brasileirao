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
import "./GolsTemporada.css";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

interface GolsTemporadaProps {
  anoSelecionado: number;
}

interface TeamSeason {
  time: string;
  gols_pro: number;
  gols_tomados: number;
}

const GolsTemporada = ({ anoSelecionado }: GolsTemporadaProps) => {
  const [data, setData] = useState<ChartData<"bar", number[], string> | null>(null);

  useEffect(() => {
    let active = true;

    fetch(`http://127.0.0.1:5000/tabela?ano=${anoSelecionado}`)
      .then((response) => response.json() as Promise<TeamSeason[]>)
      .then((teams) => {
        if (!active) return;
        const topTeams = teams
          .sort((a, b) => b.gols_pro - a.gols_pro)
          .slice(0, 10);
        setData({
          labels: topTeams.map((team) => team.time),
          datasets: [
            {
              label: "Gols pró",
              data: topTeams.map((team) => team.gols_pro),
              backgroundColor: "rgba(24, 119, 82, 0.78)",
              borderRadius: 3,
            },
            {
              label: "Gols tomados",
              data: topTeams.map((team) => team.gols_tomados),
              backgroundColor: "rgba(214, 80, 57, 0.72)",
              borderRadius: 3,
            },
          ],
        });
      })
      .catch((error) => console.error("Erro ao carregar gols:", error));

    return () => {
      active = false;
    };
  }, [anoSelecionado]);

  return (
    <section className="season-chart gols-season-chart">
      <header className="season-chart-header">
        <div>
          <h2>Produção ofensiva</h2>
          <p>Top 10 por gols marcados em {anoSelecionado}</p>
        </div>
      </header>
      {data ? (
        <Bar
          data={data}
          options={{
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: "bottom" as const } },
            scales: { x: { beginAtZero: true } },
          }}
        />
      ) : (
        <p className="season-chart-loading">Carregando...</p>
      )}
    </section>
  );
};

export default GolsTemporada;
