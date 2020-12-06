//doughnut

var dataset_percentages = JSON.parse(document.getElementById("mood_percentages").value);
console.log(typeof(dataset_percentages))
var ctxD = document.getElementById("doughnutChart").getContext('2d');
var myLineChart = new Chart(ctxD, {
type: 'doughnut',
data: {
labels: ["Very sad", "Sad", "Happy", "Very happy!"],
datasets: [{
data: dataset_percentages,
backgroundColor: ["#FF2D00", "#FF8000", "#9EFF00", "#08FF00"],
hoverBackgroundColor: ["#FF2D00", "#FF8000", "#9EFF00", "#08FF00"]
}]
},
options: {
responsive: true
}
});

//radar
var ctxR = document.getElementById("radarChart").getContext('2d');
var myRadarChart = new Chart(ctxR, {
type: 'radar',
data: {
    labels: ["Sports", "Music", "Reading", "Socializing", "Cooking", "Travelling", "Other"],
    datasets: [{
        label: "Made me the happiest",
        data: [90, 32, 10, 30, 12, 11, 20],
        backgroundColor: [
            'rgba(105, 0, 132, .2)',
        ],
        borderColor: [
            'rgba(200, 99, 132, .7)',
        ],
        borderWidth: 2
        },
    {
        label: "Made me the saddest",
        data: [28, 48, 40, 19, 20, 27, 100],
        backgroundColor: [
            'rgba(0, 250, 220, .2)',
        ],
        borderColor: [
            'rgba(0, 213, 132, .7)',
        ],
        borderWidth: 2
    }
]
},
options: {
responsive: true
}
});


//line
var dataset_moods = JSON.parse(document.getElementById("weekly_moods").value);
var ctxL = document.getElementById("lineChart").getContext('2d');
var myLineChart = new Chart(ctxL, {
type: 'line',
data: {
    labels: ["1 Dec", "2 Dec", "3 Dec", "4 Dec", "5 Dec", "6 Dec", "7 Dec"],
    datasets: [
        {
            label: "Mood per days",
            data: dataset_moods,
            backgroundColor: [
                'rgba(105, 0, 132, .2)',
            ],
            borderColor: [
                'rgba(200, 99, 132, 1)',
            ],
            borderWidth: 2
        }
    ]
},
options: {
responsive: true
}
});