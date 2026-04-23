import Chart, { Decimation }  from 'chart.js/auto'

(async function(){
    
    const data = {
        labels: [
            'Blue',
            'Red',
            'Yellow'
        ],
        datasets: [{
            labels: 'Meu primeiro dataset',
            data: [300, 50, 100],
            backgroudColor: [
                'red',
                'blue',
                'yellow'
            ],
            hoverOffset: 4
        }] 
    };
    const config = {
        type: 'doughnut',
        data: data,
    };
    const ctx = document.getElementById('gráfico_2')

    new Chart(ctx, config);

    
})();
     