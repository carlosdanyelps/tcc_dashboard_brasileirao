import { useEffect, useState } from "react";
import "./PontosTemp.css";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
);

interface PontosTempProps {
  anoSelecionado: number;
}

interface DadoApi {
  ano: number;
  pontos: number;
  time: string;
  cor: string;
  escudo?: string;
}
const PontosTemp = ({ anoSelecionado }: PontosTempProps) => {
  const [chartData, setChartData] = useState<{
    labels: string[];
    datasets: object[];
    times: string[];
  } | null>(null);
  const [loading, setLoading] = useState(true);

  const imagePlugin = {
    id: "customBarImage",
    afterDatasetsDraw(chart) {
      const { ctx, data, chartArea } = chart;
      const images = data.datasets[0].images || [];

      chart.getDatasetMeta(0).data.forEach((bar, index) => {
        const imgUrl = images[index];

        if (imgUrl && bar) {
          const img = new Image();
          img.onload = () => {
            const size = 30;
            const x = bar.x - size / 2;
            const y = bar.y - size - 8;
            
            // Verificar se está dentro do canvas
            if (y >= chartArea.top) {
              ctx.drawImage(img, x, y, size, size);
            }
          };
          img.src = imgUrl;
        }
      });
    },
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const url = `http://127.0.0.1:5000/tabela?ano=${anoSelecionado}`;
        const response = await fetch(url);
        const json = await response.json();

        const dadosApi: DadoApi[] = Array.isArray(json)
          ? json
          : json["Campeoes todas temporadas"] || json["campeoes"] || [];

        const labels = dadosApi.map((item) => item.time);
        const valores = dadosApi.map((item) => item.pontos);
        const times = dadosApi.map((item) => item.time);
        const escudos = dadosApi.map((item) => item.escudo || "");
        const cores = dadosApi.map((item) =>
          item.cor ? item.cor.replace("0.6", "0.8") : "rgba(75, 192, 192, 0.6)",
        );
        const borderColors = dadosApi.map((item) =>
          item.cor ? item.cor.replace("0.6", "1") : "rgba(75, 192, 192, 1)",
        );

        setChartData({
          labels,
          datasets: [
            {
              label: "Pontos do Campeão",
              images: escudos,
              data: valores,
              backgroundColor: cores,
              borderColor: borderColors,
              borderWidth: 1,
            },
          ],
          times,
        });
      } catch (error) {
        console.error("Erro ao buscar dados da API:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [anoSelecionado]); // Recarrega quando ano mudar

  if (loading) return <div>Carregando gráfico...</div>;
  if (!chartData) return <div>Erro ao carregar dados</div>;

  return (
    <Bar
      data={chartData}
      plugins={[imagePlugin]}
      options={{
        scales: {
            y: {
                grace: '30%'
            }
        },
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          tooltip: {
            callbacks: {
              title: () => {
                return `Ano: ${anoSelecionado}`;
              },
              label: (context) => {
                const index = context.dataIndex;
                const time = chartData?.times?.[index] ?? "Time não disponível";
                const pts = context.parsed.y;
                return `Time: ${time} | Pontos: ${pts}`;
              },
            },
          },
          legend: {
            display: true,
            position: "top" as const,
          },
        },
      }}
    />
  );
};

export default PontosTemp;
