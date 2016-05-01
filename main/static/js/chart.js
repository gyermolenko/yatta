Highcharts.setOptions({
    global: {
        useUTC: false
    }
});

 $(document).ready(function() {
    $("#chart_container").highcharts({
        xAxis: {
            type: "datetime"
        },
        chart: {
            type: "column"
        },
        series: series,
    });
});
