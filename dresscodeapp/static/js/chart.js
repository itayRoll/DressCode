//google.charts.setOnLoadCallback(drawChart);
function drawChart(fit, n_fit, p_fit, filter) {
    if (fit>0 || n_fit >0 || p_fit >0){
        var data = google.visualization.arrayToDataTable([
                      ['Vote', 'Count'],
                      ['Total Fit!', parseInt(fit)],
                      ['Sorry, your outfit is not to my liking', parseInt(n_fit)],
                      ['Your outfit is not suitable for the occasion', parseInt(p_fit)]
                    ]);
            var options = {
              //title: 'Results'
             }
            var pieContainer = document.getElementById('pie');
            var chart = new google.visualization.PieChart(pieContainer);
            chart.draw(data, options);
            var nopieContainer = document.getElementById('nopie');
            nopieContainer.style.visibility = "hidden";
        }
    else {
        noChart(filter)
    }
};

function noChart(filter) {
    var pieContainer = document.getElementById('pie')
    var nopieContainer = document.getElementById('nopie');
    pieContainer.style.visibility = "hidden";
    if (!filter) {
        nopieContainer.innerHTML = "No results yet..."
    } else {
        nopieContainer.innerHTML = "There are no results matching your filter"
    }
};

$(function(){
    var $select = $("#minAge");
    var $select2 = $("#maxAge");
    for (i=1;i<=100;i++){
        $select.append($('<option></option>').val(i).html(i))
        $select2.append($('<option></option>').val(i).html(i))
    }
});
