import { useEffect, useState } from 'react';
import './ChartAPI.css';
import { Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

interface ChartApiProps {
    anoSelecionado: number;
}

interface DadoApi {
    ano: number;
    pontos: number;
    time: string;
    cor: string;
}
const ChartAPI = ({ anoSelecionado}: ChartApiProps) => {
    const [chartData, setChartData] = useState<{ labels: string[]; datasets: object[]; times: string[] } | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const url = `http://127.0.0.1:5000/tabela?ano=${anoSelecionado}`;
                const response = await fetch(url);
                const json = await response.json();

                const dadosApi: DadoApi[] = Array.isArray(json) 
                ? json 
                : json["Campeoes todas temporadas"] || json['campeoes'] || [];

                const labels = dadosApi.map(item => item.time);
                const valores = dadosApi.map(item => item.pontos);
                const times = dadosApi.map(item => item.time);
                const cores = dadosApi.map(item => item.cor ? item.cor.replace('0.6', '0.8') : 'rgba(75, 192, 192, 0.6)');
                const borderColors = dadosApi.map(item => item.cor ? item.cor.replace('0.6', '1') : 'rgba(75, 192, 192, 1)');

                setChartData({
                    labels,
                    datasets: [
                        {
                            label: 'Pontos do Campeão',
                            data: valores,
                            backgroundColor: cores,
                            borderColor: borderColors,
                            borderWidth: 1,
                        },
                    ],
                    times,
                });
            } catch (error) {
                console.error('Erro ao buscar dados da API:', error);
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
            options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        callbacks: {
                            title: (context) => `Ano: ${context[0].label}`,
                            label: (context) => {
                                const index = context.dataIndex;
                                const time = chartData?.times?.[index] ?? 'Time não disponível';
                                const pts = context.parsed.y;
                                return `Time: ${time} | Pontos: ${pts}`;
                            },
                        },
                    },
                    legend: {
                        display: true,
                        position: 'top' as const,
                },
            },
        }}
        />
    );
};

export default ChartAPI;