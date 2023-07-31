let ctx = document.getElementById('barChart').getContext('2d');
let ctx2 = document.getElementById('scatterChart').getContext('2d');

Chart.defaults.global.animation.duration = 200;
let barChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Positive', 'Neutral', 'Negative'],
        datasets: [{
            label: 'Sentiment Count',
            barThickness: 60,
            data: sentimentCount,
            backgroundColor: ['#43AA8B', 'cyan', '#FB3640'], 
        }]
    },
    options : {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }

})

var scatterChart = new Chart(ctx2, {
    type: 'scatter',
    data: {
        datasets: [{
            label: 'Scatter Dataset',
            data: sentimentScores
        }]
    },
    
    options: {
        plugins: {
            datalabels: {
                display: false,
            }
        },
        scales: {
            /*
            xAxes: [{
                type: 'linear',
                position: 'bottom'
            }],
            */
            yAxes: [{
                display: true,
                type: 'linear',
                scaleLabel: {
                    display: true,
                    labelString: 'Subjectivity'
                }
            }],
            xAxes: [{
                display: true,
                type: 'linear',
                scaleLabel: {
                    display: true,
                    labelString: 'Polarity'
                }
            }]
        }
    }
});