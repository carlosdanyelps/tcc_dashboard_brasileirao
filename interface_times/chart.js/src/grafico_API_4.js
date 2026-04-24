import Chart from 'chart.js/auto';

(async function() {
    try {
        const [res1, res2] = await Promise.all([
            fetch('http://127.0.0.1:5000/timemain?time=Palmeiras'),
            fetch('http://127.0.0.1:5000/timemain?time=Corinthians')
        ]);
        const json1 = await res1.json();
        const json2 = await res2.json();

        const chartData = {
            labels: ['Títulos', 'Rebaixamentos'],
            datasets: [
                {
                    label: json1.time,
                    data: [json1.titulos_brasileirao, json1.rebaixamentos.length],
                    backgroundColor: 'red'
                },
                {
                    label: json2.time,
                    data: [json2.titulos_brasileirao, json2.rebaixamentos.length],
                    backgroundColor: 'blue'
                }
            ]
        };

        const config = {
            type: 'bar',
            data: chartData,
            options: {
                plugins: {
                    legend: {
                        labels: { padding: 15 }
                    }
                }
            }
        };

        const ctx = document.getElementById('grafico_API_4');
        if (!ctx) {
            console.error('Canvas "grafico_API_4" não encontrado');
            return;
        }

        const existingChart = Chart.getChart(ctx);
        if (existingChart) existingChart.destroy();

        new Chart(ctx, config);
    } catch (error) {
        console.error('Erro ao montar o gráfico:', error);
    }
})();