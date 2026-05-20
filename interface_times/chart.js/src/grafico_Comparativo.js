import Chart from 'chart.js/auto';
import DataLabelsPlugin from 'chartjs-plugin-datalabels';

Chart.register(DataLabelsPlugin);

(async function(){
    try {
        const [res1, res2] = await Promise.all([
            fetch('http://127.0.0.1:5000/timemain?time=Flamengo'),
            fetch('http://127.0.0.1:5000/timemain?time=Palmeiras')
        ]);

        const json1 = await res1.json();
        const json2 = await res2.json();

        const chartData = {
            labels: ['Vitórias', 'Derrotas', 'Gols', 'Empates'],
            datasets: [
                {
                    label: json1.time,
                    data: [json1.vitorias, json1.derrotas, json1.gols, json1.empate],
                    backgroundColor: json1.cor,
                    borderColor: json1.bordaCor,
                    borderWidth: 2
                },
                {
                    label: json2.time,
                    data: [json2.vitorias, json2.derrotas, json2.gols, json2.empate],
                    backgroundColor: json2.cor,
                    borderColor: json2.bordaCor,
                    borderWidth: 2
                }
            ]
        };

        const config = {
            type: 'bar',
            data: chartData,
            options: {
                indexAxis: 'y',
                responsive: true,
                animation: {
                    duration: 1200,
                    easing: 'easeInOutQuart'
                },
                plugins: {
                    legend: { position: 'top' },
                    title: {
                        display: true,
                        text: `Comparativo de Times - ${json1.time} vs ${json2.time}`,
                        font: { size: 16, weight: 'bold' }
                    },
                    datalabels: {
                        anchor: 'end',
                        align: 'end',
                        color: (context) => context.dataset.borderColor,
                        font: { weight: 'bold', size: 12 },
                        formatter: (value) => value
                    }
                }
            }
        };

        const ctx = document.getElementById('grafico_Comparativo');
        const existing = Chart.getChart(ctx);
        if (existing) existing.destroy();
        new Chart(ctx, config);

    } catch (erro) {
        console.error('Erro ao buscar dados:', erro);
    }
})();
