import Chart from 'chart.js/auto';

(async function() {
    try {
        const [res1, res2] = await Promise.all([
            fetch('http://127.0.0.1:5000/pontuacao_temporada?time=Flamengo'),
            fetch('http://127.0.0.1:5000/pontuacao_temporada?time=Palmeiras')
        ]);

        const json1 = await res1.json();
        const json2 = await res2.json();
        
        const chartData = {
            labels: json1.anos || ['pontos_por_temporada'],
            datasets: [
                {
                    label: json1.time,
                    data: json1.pontos_por_temporada, 
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.3,
                    fill: true
                },
                {   
                    label: json2.time,
                    data: json2.pontos_por_temporada,
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    tension: 0.3,
                    fill: true
                }
            ]
        };

        const config = {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'top' },
                    title: {
                        display: true,
                        text: 'Comparativo de Desempenho'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        title: { display: true, text: 'Pontuação' }
                    },
                    x: {
                        title: { display: true, text: 'Temporadas' }
                    }
                }
            }
        };

        const ctx = document.getElementById('grafico_API2');
        if (!ctx) {
            console.error('Canvas "grafico_API2" não encontrado');
            return;
        }
        
        const existingChart = Chart.getChart(ctx);
        if (existingChart) existingChart.destroy();
        
        new Chart(ctx, config);
    } catch (error) {
        console.error('Erro ao montar o gráfico:', error);
    }
})();