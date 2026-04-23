import Chart, { Decimation, plugins }  from 'chart.js/auto'

(async function(){
        const data = {
        labels: [
            'flamengo',
            'palmeiras',
            'santos'
        ],
        datasets: [{
            labels: ['flamengo', 'palmeiras', 'santos'],
            data: [56, 50, 67],
            backgroundColor: [
                'red',
                'green',
                'black'
            ],
            hoverBackgroundColor: [
                'lightcoral',
                'lightgreen',
                'gray'
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
        hoverOffset: 60
    }
};
    const ctx = document.getElementById('grafico_3')

    new Chart(ctx, config);

    
})();
     