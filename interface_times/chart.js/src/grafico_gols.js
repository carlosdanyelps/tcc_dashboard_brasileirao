import Chart, { Decimation }  from 'chart.js/auto'

(async function(){
    try{

        const url = 'http://127.0.0.1:5000/tabela?time=Flamengo&ano=2023';

        const response = await fetch(url);

        const json = (await response.json())[0];

        const data = {
            labels: ['Gols Pró', 'Gols Tomados', 'Saldo'],
            datasets: [
                {
                    label: json.time,
                    data: [json.gols_pro, json.gols_tomados, json.saldo],
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.85)',
                        'rgba(255, 99, 132, 0.85)',
                        'rgba(75, 192, 192, 0.85)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(75, 192, 192, 1)'
                    ],
                    borderWidth: 2,
                    hoverOffset: 20,
                    hoverBorderWidth: 3
                }
            ]
        };

        const config = {
            type: 'pie',
            data: data,
            options: {
                animation: {
                    animateRotate: true,
                    animateScale: true,
                    duration: 1200,
                    easing: 'easeInOutQuart'
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            font: { size: 14, weight: 'bold' },
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    title: {
                        display: true,
                        text: `Estatísticas de Gols - ${json.time} (${json.temporada})`,
                        font: { size: 16, weight: 'bold' },
                        padding: { bottom: 15 }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const pct = ((context.parsed / total) * 100).toFixed(1);
                                return ` ${context.label}: ${context.parsed} (${pct}%)`;
                            }
                        }
                    },
                    datalabels: { display: false }
                }
            }
        };
        
        const ctx = document.getElementById('grafico_gols');
        const existing = Chart.getChart(ctx);
        if (existing) existing.destroy();
        const myChart = new Chart(ctx, config)
        
        
        
            } catch (erro) {
                console.error("Erro ao buscar dados:", erro);
            }
})();