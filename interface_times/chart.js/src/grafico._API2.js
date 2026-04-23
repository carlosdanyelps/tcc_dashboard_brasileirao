import Chart from 'chart.js/auto';

(async function() {
    try {
        const url = 'http://192.168.200.170:8080/timemain/time_main';
        const resposta = await fetch(url);
    
        if (!resposta.ok) {
            throw new Error(`Erro na requisição: ${resposta.status}`);
        }
        const json = await resposta.json();

        const dadosApi = Array.isArray(json)

            ? json

            : json['Resumo do Time'] || json['resumo_time'] || [];


        const labels = dadosApi.map(item => item.time);

        const valores = dadosApi.map(item => item.gols);


        const data = {
            labels: labels,
            datasets: [{
                data: valores,
                backgroundColor: [
                    'red',
                    'green',
                    'black',
                    'blue',
                    'yellow',
                    'purple',
                    
                    
                ],
                hoverBackgroundColor: [
                    'lightcoral',
                    'lightgreen',
                    'gray',
                    'lightblue',
                    'lightyellow',
                    'plum',
                ]
            }] 
        };
            const config = {
            type: 'pie',
            data: data,
            options: {
                plugins: {
                    legend: {
                        labels: { padding: 15 }
                    }
                },
                hoverOffset: 200
            }
        };
            const ctx = document.getElementById('grafico_API2')
        
            new Chart(ctx, config);
        
            
    } catch (erro) {
        console.error("Falha ao carregar o gráfico:", erro);
    }
})();
             