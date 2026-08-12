import { useEffect, useState, useRef, use } from "react";
import "./ComparativoTimes.css";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
);

interface ComparativosTimesProps {
  anoSelecionado: number;
}

interface DadoApi {
  ano: number;
  pontos: number;
  time: string;
  cor: string;
  escudo: string;
}

const ComparativosTimes = ({ anoSelecionado }: ComparativosTimesProps) => {
  const [chartData, setChartData] = useState<{
    labels: string[];
    datasets: object[];
    times: string[];
  } | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const chartRef = useRef<any>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const top4response = await fetch(
          `http://127.0.0.1:5000/tabela?ano=${anoSelecionado}&limite=4`,
        );
        const top4: DadoApi[] = await top4response.json();

        if (!Array.isArray(top4) || top4.length === 0) {
          throw new Error("Nenhum time top 4 retornado pela API");
        }

        const top4Times = top4.slice(0, 4).map((item) => item.time);

        const response = await fetch(
          `http://127.0.0.1:5000/tabela/rodada?ano=${anoSelecionado}`,
        );
        const allData = await response.json();

        if (!Array.isArray(allData) || allData.length === 0) {
          throw new Error("Nenhum dado retornado da API de rodadas");
        }

        // 3. Filtrar apenas dados dos 4 primeiros times
        const json = allData.filter((item) => top4Times.includes(item.time));
        const rodadas = Array.from(
          new Set(json.map((item) => item.rodada)),
        ).sort((a, b) => a - b);

        // 4. Mapear cores dos times
        const teamsWithColors = top4.reduce((acc, item) => {
          acc[item.time] = {
            cor: item.cor || "rgba(75, 192, 192, 1)",
            bordaCor: item.bordaCor || "rgba(54, 162, 235, 1)",
          };
          return acc;
        }, {});

        // 5. Montar os Datasets
        const datasets = top4Times.map((time) => {
          const timeData = json
            .filter((item) => item.time === time)
            .reduce((acc, item) => {
              acc[item.rodada] = item.posicao;
              return acc;
            }, {});

          const teamColor = teamsWithColors[time] || {
            cor: "rgba(75, 192, 192, 1)",
            bordaCor: "rgba(54, 162, 235, 1)",
          };

          return {
            label: time,
            data: rodadas.map((rodada) => timeData[rodada] ?? null),
            borderColor: teamColor.bordaCor,
            backgroundColor: teamColor.cor,
            pointBackgroundColor: teamColor.cor,
            pointBorderColor: teamColor.bordaCor,
            fill: false,
            tension: 0.3,
            pointRadius: 3,
            borderWidth: 2,
          };
        });

        // 6. Atualizar o estado com o formato aceito pelo Chart.js
        setChartData({
          labels: rodadas.map((rodada) => ` ${rodada}`),
          datasets,
        });
      } catch (err) {
        console.error("Erro ao buscar dados:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [anoSelecionado]);

  // Opções de configuração do gráfico (as mesmas que você já usava)
  const options = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: "Posição por Rodada - Top 4 Times",
        font: { size: 16, weight: "bold" },
      },
      legend: {
        position: "top",
        labels: { boxWidth: 12, padding: 12 },
      },
    },
    scales: {
      y: {
        reverse: true, // Mantém o 1º lugar no topo
        min: 0,
        max: 20,
        autoSkip: false,
        title: { display: true, text: "Posição" },
      },
      x: {
        title: { display: true, text: "Rodada" },
        ticks: { autoSkip: false },
      },
    },
  };

  if (loading) return <div>Carregando gráfico...</div>;
  if (error) return <div>Erro ao carregar dados: {error}</div>;

  return (
    <div style={{ width: "100%", maxWidth: "100%", margin: "0 auto" }}>
      {chartData && <Line data={chartData} options={options} />}
    </div>
  );
};

export default ComparativosTimes