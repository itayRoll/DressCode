function drawChart(fit, n_fit, p_fit,s_fit, s_n_fit, s_p_fit, filter) {
    if (fit>0 || n_fit >0 || p_fit >0) {
        var data = google.visualization.arrayToDataTable([
                      ['Vote', 'Count'],
                      ['Total Fit!', parseInt(fit)],
                      ['Like your outfit but not for the occasion', parseInt(p_fit)],
                      ['Sorry, your outfit is not to my liking', parseInt(n_fit)]
                    ]);
      var similar_data = google.visualization.arrayToDataTable([
              ['Vote', 'Count'],
              ['Total Fit!', parseInt(s_fit)],
              ['Like your outfit but not for the occasion', parseInt(s_p_fit)],
              ['Sorry, your outfit is not to my liking', parseInt(s_n_fit)]
            ]);
        var options = {
            width: 480,
            height: 240,
            'chartArea': {'width': '95%', 'height': '80%'},
            colors: ['#68c47c', '#a39a99', '#f95967'], // green red grey
            pieSliceTextStyle: {
                color: 'black',
            },
            'legend':'left'
         }
        var pieContainer = document.getElementById('pie');
        var chart = new google.visualization.PieChart(pieContainer);
        chart.draw(data, options);
        var nopieContainer = document.getElementById('nopie');
        nopieContainer.style.visibility = "hidden";

        if (s_fit>0 || s_n_fit >0 || s_p_fit >0) {
            var similarPieContainer = document.getElementById('pie2');
            var chart2 = new google.visualization.PieChart(similarPieContainer);
            chart2.draw(similar_data, options);
            var nopieContainer2 = document.getElementById('nopie2');
            nopieContainer2.style.visibility = "hidden";
        } else {
            noSimilarChart(filter)
        }
    }
    else {
        noChart(filter)
        noSimilarChart(filter)
    }
};

function noChart(filter) {
    var pieContainer = document.getElementById('pie')
    var nopieContainer = document.getElementById('nopie');
    pieContainer.style.visibility = "hidden";
};

function noSimilarChart(filter) {
    var pieContainer = document.getElementById('pie2')
    var nopieContainer = document.getElementById('nopie2');
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
