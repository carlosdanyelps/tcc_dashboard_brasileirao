import { useEffect, useState } from "react";
import "./Gols.css";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

interface GolsProps {
  timeSelected?: string;
}

interface DadoApi {
  time: string;
  gols_pro: number;
  gols_tomados: number;
  saldo: number;
  temporada: number;
}

const Gols = ({ timeSelected = "Flamengo" }: GolsProps) => {
  const [chartData, setChartData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [timeInfo, setTimeInfo] = useState<any>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const url = `http://127.0.0.1:5000/tabela?time=${timeSelected}&ano=2024`;
        const response = await fetch(url);
        const json = await response.json();

        const data: DadoApi[] = Array.isArray(json) ? json : [json];
        const dadoTime = data[0];

        if (dadoTime) {
          setTimeInfo(dadoTime);
          setChartData({
            labels: ["Gols Pró", "Gols Tomados", "Saldo"],
            datasets: [
              {
                data: [dadoTime.gols_pro, dadoTime.gols_tomados, dadoTime.saldo],
                backgroundColor: [
                  "rgba(76, 175, 80, 0.8)",
                  "rgba(244, 67, 54, 0.8)",
                  "rgba(33, 150, 243, 0.8)",
                ],
                borderColor: [
                  "rgba(76, 175, 80, 1)",
                  "rgba(244, 67, 54, 1)",
                  "rgba(33, 150, 243, 1)",
                ],
                borderWidth: 1,
              },
            ],
          });
        }
      } catch (error) {
        console.error("Erro ao buscar dados:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [timeSelected]);

  if (loading) {
    return <div className="chart-loading">Carregando...</div>;
  }

  return (
    <div className="gols-container">
      <div className="chart-header">
        <h2>Estatísticas de Gols</h2>
        <p>{timeInfo?.time || timeSelected}</p>
      </div>
      {chartData ? (
        <div className="gols-chart-wrapper">
          <Pie
            data={chartData}
            options={{
              responsive: true,
              maintainAspectRatio: true,
              plugins: {
                legend: {
                  position: "bottom" as const,
                  labels: {
                    padding: 10,
                    font: { size: 12 },
                  },
                },
              },
            }}
          />
        </div>
      ) : (
        <p>Erro ao carregar dados</p>
      )}
    </div>
  );
};

export default Gols;
