import { useEffect, useState } from "react";
import "./Campeoes.css";
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

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface CampoesProps {
  anoSelecionado: number;
}

interface DadoApi {
  ano: number;
  pontos: number;
  time: string;
  cor: string;
  escudo: string;
}

const Campeoes = ({ anoSelecionado }: CampoesProps) => {
  const [chartData, setChartData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const url = `http://127.0.0.1:5000/tabela?ano=${anoSelecionado}`;
        const response = await fetch(url);
        const json = await response.json();

        const dadosApi: DadoApi[] = Array.isArray(json)
          ? json
          : json["Campeoes todas temporadas"] || json["campeoes"] || [];

        const labels = dadosApi.map((item) => item.time);
        const valores = dadosApi.map((item) => item.pontos);
        const cores = dadosApi.map((item) =>
          item.cor ? item.cor.replace("0.6", "0.7") : "rgba(75, 192, 192, 0.7)"
        );
        const borderColors = dadosApi.map((item) =>
          item.cor ? item.cor.replace("0.6", "1") : "rgba(75, 192, 192, 1)"
        );

        setChartData({
          labels,
          datasets: [
            {
              label: "Pontos",
              data: valores,
              backgroundColor: cores,
              borderColor: borderColors,
              borderWidth: 1,
            },
          ],
        });
      } catch (error) {
        console.error("Erro ao buscar dados:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [anoSelecionado]);

  if (loading) {
    return <div className="chart-loading">Carregando...</div>;
  }

  return (
    <div className="campeoes-container">
      <div className="chart-header">
        <h2>Campeões - {anoSelecionado}</h2>
        <p>Pontos da temporada</p>
      </div>
      {chartData ? (
        <Bar
          data={chartData}
          options={{
            indexAxis: "x" as const,
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
              legend: { display: false },
            },
            scales: {
              y: {
                beginAtZero: true,
              },
            },
          }}
        />
      ) : (
        <p>Erro ao carregar dados</p>
      )}
    </div>
  );
};

export default Campeoes;
