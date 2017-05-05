//google.charts.setOnLoadCallback(drawChart);
function drawChart(fit, n_fit, p_fit, filter) {
    if (fit>0 || n_fit >0 || p_fit >0){
        var data = google.visualization.arrayToDataTable([
                      ['Vote', 'Count'],
                      ['Total Fit!', parseInt(fit)],
                      ['Like your outfit but not for the occasion', parseInt(p_fit)],
                      ['Sorry, your outfit is not to my liking', parseInt(n_fit)]
                    ]);
            var options = {
                width: 480,
                height: 240,
                'chartArea': {'width': '95%', 'height': '80%'},
                //colors: ['#e0440e', '#ec8f6e', '#f6c7b6'],
                colors: ['#6eecb8', '#9bf2ce', '#c9f8e4'],
                pieSliceTextStyle: {
                    color: 'black',
                },
                'legend':'left'
             }
            var pieContainer = document.getElementById('pie');
            var chart = new google.visualization.PieChart(pieContainer);
            chart.draw(data, options);

            var pieContainer2 = document.getElementById('pie2');
            var chart2 = new google.visualization.PieChart(pieContainer2);
            chart2.draw(data, options);

            var nopieContainer = document.getElementById('nopie');
            nopieContainer.style.visibility = "hidden";

            var nopieContainer2 = document.getElementById('nopie2');
            nopieContainer2.style.visibility = "hidden";
        }
    else {
        noChart(filter)
    }
};

function noChart(filter) {
    var pieContainer = document.getElementById('pie')
    var nopieContainer = document.getElementById('nopie');
    pieContainer.style.visibility = "hidden";
};

$(function(){
    var $select = $("#minAge");
    var $select2 = $("#maxAge");
    for (i=1;i<=100;i++){
        $select.append($('<option></option>').val(i).html(i))
        $select2.append($('<option></option>').val(i).html(i))
    }
});
