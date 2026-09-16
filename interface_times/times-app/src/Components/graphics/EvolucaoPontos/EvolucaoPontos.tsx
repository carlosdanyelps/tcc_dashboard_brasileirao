import { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Tooltip,
} from "chart.js";
import type { ChartData } from "chart.js";
import "./EvolucaoPontos.css";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

interface EvolucaoPontosProps {
  anoSelecionado: number;
}

interface ClassificationTeam {
  time: string;
  pontos: number;
}

interface RoundTeam extends ClassificationTeam {
  rodada: number;
}

const COLORS = ["#187752", "#d65039", "#2563a6", "#b17d1d", "#6d4c8d"];

const EvolucaoPontos = ({ anoSelecionado }: EvolucaoPontosProps) => {
  const [data, setData] = useState<ChartData<"line", number[], string> | null>(null);

  useEffect(() => {
    let active = true;

    Promise.all([
      fetch(`http://127.0.0.1:5000/tabela?ano=${anoSelecionado}`),
      fetch(`http://127.0.0.1:5000/tabela/rodada?ano=${anoSelecionado}`),
    ])
      .then(async ([classificationResponse, roundsResponse]) => {
        if (!classificationResponse.ok || !roundsResponse.ok) {
          throw new Error("Não foi possível carregar a evolução da temporada");
        }
        return {
          classification: (await classificationResponse.json()) as ClassificationTeam[],
          rounds: (await roundsResponse.json()) as RoundTeam[],
        };
      })
      .then(({ classification, rounds }) => {
        if (!active) return;
        const topTeams = classification.slice(0, 5).map((team) => team.time);
        const roundNumbers = Array.from(new Set(rounds.map((item) => item.rodada))).sort(
          (a, b) => a - b,
        );

        setData({
          labels: roundNumbers.map(String),
          datasets: topTeams.map((team, index) => ({
            label: team,
            data: roundNumbers.map(
              (round) =>
                rounds.find((item) => item.time === team && item.rodada === round)?.pontos ?? null,
            ),
            borderColor: COLORS[index],
            backgroundColor: COLORS[index],
            pointRadius: 2,
            borderWidth: 2,
            tension: 0.25,
            spanGaps: true,
          })),
        });
      })
      .catch((error) => console.error("Erro ao carregar evolução:", error));

    return () => {
      active = false;
    };
  }, [anoSelecionado]);

  return (
    <section className="season-chart evolution-chart">
      <header className="season-chart-header">
        <h2>Corrida pelo topo</h2>
        <p>Pontos acumulados por rodada em {anoSelecionado}</p>
      </header>
      {data ? (
        <Line
          data={data}
          options={{
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: "index", intersect: false },
            scales: { y: { beginAtZero: true }, x: { title: { display: true, text: "Rodada" } } },
            plugins: { legend: { position: "bottom" as const } },
          }}
        />
      ) : (
        <p className="season-chart-loading">Carregando...</p>
      )}
    </section>
  );
};

export default EvolucaoPontos;
