import Chart from 'chart.js/auto';

(async function() {
    try {
        const [res1, res2] = await Promise.all([
            fetch('http://127.0.0.1:5000/estatisticas?time=Flamengo'),
            fetch('http://127.0.0.1:5000/estatisticas?time=Criciúma')
        ]);
        const json1 = await res1.json();
        const json2 = await res2.json();
    
        // Dados do gráfico
        const chartData = {
            labels: json1.media || [' Média de Empates', 'Média de Vitórias', 'Média de Derrotas'],
            datasets: [
                {
                    label: json1.time,
                    data: [json1.média_empates, json1.média_vitórias, json1.média_derrotas],
                    borderColor: json1.cor,
                    backgroundColor: json1.bordaCor,
                    borderWidth: 4
                },
                {
                    label: json2.time,
                    data: [json2.média_empates, json2.média_vitórias, json2.média_derrotas],
                    borderColor: json2.cor,
                    backgroundColor: json2.bordaCor,
                    borderWidth: 4
                }
            ]
        };

        const config = {
            type: 'radar',
            data: chartData,
            options: {
                animation: {
                    duration: 1200,
                    easing: 'easeInOutQuart'
                },
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            font: {
                                size: 15,
                                weight: 'normal'
                            },
                            padding: 15
                        }
                    },
                    title: {
                        display: true,
                        text: 'Comparativo de Times',
                        font: {
                            size: 16,
                            weight: 'bold'
                        },
                        padding: 10
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.parsed.r;
                            }
                        }
                    },
                    datalabels: { display: false }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        ticks: {
                            display: true,
                            stepSize: 100,
                            font: {
                                size: 12
                            }
                        },
                        grid: {
                            display: true,
                            drawBorder: true
                        }
                    }
                }
            }
        };

        const ctx = document.getElementById('graficos_Medias');
        const myChart = new Chart(ctx, config)



    } catch (erro) {
        console.error("Erro ao buscar dados:", erro);
    }
})();