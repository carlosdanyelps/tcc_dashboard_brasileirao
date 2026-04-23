import Chart from 'chart.js/auto';

(async function() {
    try {
        const url = 'http://127.0.0.1:5000/tabela?ano=2019';
        
        const resposta = await fetch(url);
    
        const json = await resposta.json();

        const dadosApi = Array.isArray(json)
            ? json

            : json['Campeoes todas temporadas'] || json['campeoes'] || [];

        const labels = dadosApi.map(item => item.ano);

        const valores = dadosApi.map(item => item.pontos);

        new Chart(
            document.getElementById('grafico_API'),
            {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Pontos do Campeão',
                        data: valores,
                        backgroundColor: 'red',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        tooltip: {
                            callbacks: { 
                                title: (context) => `Ano: ${context[0].label}`,
                                
                                label: (context) => {
                                    const index = context.dataIndex;
                                    const time = dadosApi[index].time;
                                    const pts = context.parsed.y;
                                    return ` Time: ${time} | Pontos: ${pts}`;
                                }
                            }
                        }
                    }
                }
            }
        );
    } catch (erro) {
        console.error("Falha ao carregar o gráfico:", erro);
    }
})();