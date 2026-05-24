import Chart from 'chart.js/auto';

(async function(){
    try {
        const top4Response = await fetch('http://127.0.0.1:5000/tabela?ano=2010&limit=4');
        const top4 = await top4Response.json();

        if (!Array.isArray(top4) || top4.length === 0) {
            throw new Error('Nenhum time top 4 retornado da API');
        }

        const top4Times = top4.slice(0, 4).map(item => item.time);
        const response = await fetch('http://127.0.0.1:5000/tabela/rodada?ano=2010');
        const allData = await response.json();

        if (!Array.isArray(allData) || allData.length === 0) {
            throw new Error('Nenhum dado retornado da API de rodadas');
        }

        // Filtrar apenas dados dos 4 primeiros times
        const json = allData.filter(item => top4Times.includes(item.time));

        const rodadas = Array.from(new Set(json.map(item => item.rodada))).sort((a, b) => a - b);

        const teamsWithColors = top4.reduce((acc, item) => {
            acc[item.time] = {
                cor: item.cor || 'rgba(75, 192, 192, 1)',
                bordaCor: item.bordaCor || 'rgba(54, 162, 235, 1)'
            };
            return acc;
        }, {});

        const datasets = top4Times.map((time) => {
            const timeData = json
                .filter(item => item.time === time)
                .reduce((acc, item) => {
                    acc[item.rodada] = item.posicao;
                    return acc;
                }, {});

            const teamColor = teamsWithColors[time] || {
                cor: 'rgba(75, 192, 192, 1)',
                bordaCor: 'rgba(54, 162, 235, 1)'
            };

            return {
                label: time,
                data: rodadas.map(rodada => timeData[rodada] ?? null),
                borderColor: teamColor.bordaCor,
                backgroundColor: teamColor.cor,
                pointBackgroundColor: teamColor.cor,
                pointBorderColor: teamColor.bordaCor,
                fill: false,
                tension: 0.3,
                pointRadius: 3,
                borderWidth: 2
            };
        });

        const config = {
            type: 'line',
            data: {
                labels: rodadas.map(rodada => `Rodada ${rodada}`),
                datasets
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Posição por Rodada - Top 4 Times',
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: {
                        position: 'top',
                        labels: { boxWidth: 12, padding: 12 }
                    }
                },
                scales: {
                    y: {
                        reverse: true,
                        min: 1,
                        max: 20,
                        autoSkip: false,
                        title: { display: true, text: 'Posição' }
                    },
                    x: {
                        title: { display: true, text: 'Rodada' }
                    }
                }
            }
        };

        const ctx = document.getElementById('grafico_Desempenho2');
        const existing = Chart.getChart(ctx);
        if (existing) existing.destroy();
        new Chart(ctx, config);

    } catch (erro) {
        console.error('Erro ao buscar dados:', erro);
    }
}());
