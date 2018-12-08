<script>
var myChart = new Chart(document.getElementById("myChart"), {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Sensor 1',
            borderColor: "#FF0000",
            data: sensor1,
            fill: false,
            pointRadius: 1
        }, {
           label: 'Sensor 2',
            borderColor: "#0000FF",
            data: sensor2,
            fill: false,
            pointRadius: 1
        }]
    },
    options: {
        title: {
            display: true,
            text: 'Temperature'
        },
        animation: false,
        scales: {
            yAxes: [{
                scaleLabel: {
                    labelString: 'Degrees Celsius',
                    display: true,
                },
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 70
                }
            }],
            xAxes: [{
                scaleLabel: {
                    labelString: 'Minutes',
                    display: true
                },
                //display: false,
                ticks: {
                    display: false,
                    maxTicksLimit: 30
                }
            }]
        }
    }
});
</script>
