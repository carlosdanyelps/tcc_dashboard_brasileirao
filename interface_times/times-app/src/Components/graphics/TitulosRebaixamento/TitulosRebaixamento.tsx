import { useEffect, useState } from "react";
import "./TitulosRebaixamento.css";
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
  Legend
);

interface TimeData {
  time: string;
  titulos_brasileirao: number;
  rebaixamentos: any[];
  cor: string;
  bordaCor: string;
}

interface TitulosRebaixamentoProps {
  times?: string[];
}

const TitulosRebaixamento = ({ times = ["Palmeiras", "Corinthians"] }: TitulosRebaixamentoProps) => {
  const [chartData, setChartData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const responses = await Promise.all(
          times.map((time) =>
            fetch(`http://127.0.0.1:5000/timemain?time=${time}`)
          )
        );

        const timesData: TimeData[] = await Promise.all(
          responses.map((res) => res.json())
        );

        const labels = ["Títulos", "Rebaixamentos"];
        const datasets = timesData.map((time, index) => ({
          label: time.time,
          data: [time.titulos_brasileirao, time.rebaixamentos.length],
          backgroundColor: time.cor || `hsl(${index * 120}, 70%, 50%)`,
          borderColor: time.bordaCor || `hsl(${index * 120}, 100%, 50%)`,
          borderWidth: 1,
        }));

        setChartData({
          labels,
          datasets,
        });
      } catch (error) {
        console.error("Erro ao buscar dados:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [times]);

  if (loading) {
    return <div className="chart-loading">Carregando...</div>;
  }

  return (
    <div className="titulos-container">
      <div className="chart-header">
        <h2>Títulos & Rebaixamentos</h2>
        <p>Comparativo histórico</p>
      </div>
      {chartData ? (
        <Bar
          data={chartData}
          options={{
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
              legend: {
                position: "top" as const,
                labels: {
                  padding: 10,
                  font: { size: 12 },
                },
              },
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

export default TitulosRebaixamento;
