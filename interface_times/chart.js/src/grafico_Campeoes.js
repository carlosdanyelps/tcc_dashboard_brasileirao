import Chart from 'chart.js/auto';

(async function() {
    try {
        const url = 'http://127.0.0.1:5000/tabela?ano=2023';
        
        const resposta = await fetch(url);
    
        const json = await resposta.json();

        const dadosApi = Array.isArray(json)
            ? json

            : json['Campeoes todas temporadas'] || json['campeoes'] || [];

        const labels = dadosApi.map(item => item.time);

        const valores = dadosApi.map(item => item.pontos);

        new Chart(
            document.getElementById('grafico_Campeoes'),
            {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Pontos da Rodada',
                        data: valores,
                        backgroundColor: ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)'],
                        borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)'],
                        borderWidth: 1,
                    }],
                },
                options: {
                    responsive: true,
                    animation: {
                        duration: 1200,
                        easing: 'easeInOutQuart'
                    },
                    plugins: {
                        tooltip: {
                            callbacks: { 
                                title: (context) => {
                                    const index = context[0].dataIndex;
                                    const ano = dadosApi[index].ano || null;
                                    return `Ano: ${ano}`;
                                },
                                
                                label: (context) => {
                                    const index = context.dataIndex;
                                    const time = dadosApi[index].time;
                                    const pts = context.parsed.y;
                                    return ` Time: ${time} | Pontos: ${pts}`;
                                }
                            }
                        },
                        datalabels: { display: false }
                    }
                }
            }
        );
    } catch (erro) {
        console.error("Falha ao carregar o gráfico:", erro);
    }
})();