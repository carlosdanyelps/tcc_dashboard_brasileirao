import { useEffect, useState } from "react";
import "./Desempenho.css";
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
  Legend
);

interface DesempenhoProps {
  times?: string[];
}

interface TeamSummary {
  time: string;
}

interface TimePerformance {
  time: string;
  anos: number[];
  pontos_por_temporada: number[];
  cor: string;
  bordaCor: string;
}

const DEFAULT_TIMES = ["Flamengo", "Palmeiras"];

const Desempenho = ({ times = DEFAULT_TIMES }: DesempenhoProps) => {
  const [chartData, setChartData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [availableTeams, setAvailableTeams] = useState<string[]>(DEFAULT_TIMES);
  const [selectedTimes, setSelectedTimes] = useState<string[]>(() =>
    times.length >= 2 ? times.slice(0, 2) : DEFAULT_TIMES
  );

  useEffect(() => {
    let isMounted = true;

    fetch("http://127.0.0.1:5000/timemain/time_main")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Não foi possível carregar os times");
        }
        return response.json() as Promise<TeamSummary[]>;
      })
      .then((teams) => {
        if (isMounted) {
          setAvailableTeams(teams.map((team) => team.time));
        }
      })
      .catch((error) => {
        console.error("Erro ao buscar times:", error);
      });

    return () => {
      isMounted = false;
    };
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const responses = await Promise.all(
          selectedTimes.map((time) =>
            fetch(
              `http://127.0.0.1:5000/pontuacao_temporada?time=${time}`
            )
          )
        );

        const timesData: TimePerformance[] = await Promise.all(
          responses.map((res) => res.json())
        );

        // Get unique years
        const allYears = new Set<number>();
        timesData.forEach((time) => {
          (time.anos || []).forEach((year) => allYears.add(year));
        });
        const sortedYears = Array.from(allYears).sort();

        const datasets = timesData.map((time, index) => ({
          label: time.time,
          data: time.pontos_por_temporada || [],
          borderColor: time.cor || `hsl(${index * 120}, 70%, 50%)`,
          backgroundColor: time.cor?.replace("0.6", "0.1") || `hsla(${index * 120}, 70%, 50%, 0.1)`,
          borderWidth: 2,
          fill: true,
          tension: 0.3,
          pointRadius: 3,
          pointBorderWidth: 0,
        }));

        setChartData({
          labels: sortedYears.map((year) => year.toString()),
          datasets,
        });
      } catch (error) {
        console.error("Erro ao buscar dados:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [selectedTimes]);

  if (loading) {
    return <div className="chart-loading">Carregando...</div>;
  }

  return (
    <div className="desempenho-container">
      <div className="chart-header">
        <div>
          <h2>Desempenho ao Longo do Tempo</h2>
          <p>Pontos por temporada</p>
        </div>
        <div className="team-selectors">
          {selectedTimes.map((selectedTime, index) => (
            <label key={index}>
              Time {index + 1}
              <select
                value={selectedTime}
                onChange={(event) => {
                  const newTimes = [...selectedTimes];
                  newTimes[index] = event.target.value;
                  setSelectedTimes(newTimes);
                }}
              >
                {availableTeams.map((team) => (
                  <option
                    key={team}
                    value={team}
                    disabled={selectedTimes.some(
                      (otherTime, otherIndex) =>
                        otherIndex !== index && otherTime === team
                    )}
                  >
                    {team}
                  </option>
                ))}
              </select>
            </label>
          ))}
        </div>
      </div>
      {chartData ? (
        <Line
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
                  usePointStyle: true,
                  pointStyle: "circle",
                },
              },
            },
            scales: {
              y: {
                beginAtZero: true,
              },
              x: {
                grid: {
                  display: false,
                },
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

export default Desempenho;
