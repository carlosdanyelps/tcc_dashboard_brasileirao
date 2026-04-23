import Chart, { Decimation }  from 'chart.js/auto'
(async function() {
    const data= [
        {year: 2010, count: 81 },
        {year: 2011, count: 20 },
        {year: 2012, count: 15 },
        {year: 2013, count: 25 },
        {year: 2014, count: 22 },
        {year: 2015, count: 30 },
        {year: 2016, count: 28 },
        
    ];

    let color = 'red'

    new Chart(
        document.getElementById('gráfico_1'),
        {
            type: 'bar',
            data: {
                labels: data.map(row => row.year),
                datasets: [
                    {
                        label: 'gráfico_1 by year',
                        data: data.map(row => row.count),
                        backgroundColor: color,
                        borderRadius: 70,
                        borderWidth: 10,
                        borderColor: '#ff00002c'
                    }
                ]
            }
        }
    );
})();
