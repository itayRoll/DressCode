var numOfCalls = 0
function postAnswer(questionId, vote, userScore){
    numOfCalls = numOfCalls+1
	// add loading animation to button
	$('#thanks'+questionId).show()
	$('#question'+questionId).hide()
    var itemsNotAsPic = false
	if ($('#checkbox'+questionId)[0].checked) {
        itemsNotAsPic = true
	}
	$('#thanks'+questionId).fadeOut(1000)
	var numOfVisibleRows = $('#questions_table tr:visible').length
	var thankyou = 'Thanks for answering!';
	var text = userScore > 10 ? '\nYou have enough credit. Post!' : 'Only '+ (10 - userScore) + ' to go';
	$('#msgText'+questionId).text(thankyou+text);
	if (numOfCalls == numOfVisibleRows)
	{
	$('#reload').show()
	}
	$.ajax({
				url: "/post-answer/",
				type: 'POST',
				data: {
					'question_id': questionId,
					'vote': vote,
					'itemsNotAsPic': itemsNotAsPic,
					csrfmiddlewaretoken: CSRF_TOKEN,
				},
			success: function(response) {
  				result = JSON.parse(response);  // Get the results sended from ajax to here
  				if (result.error) {
      				// Error
      				alert(result.error_text);
  				} else {
              		// Success
      			}
  			}
		});
}
function reload() {
	location.reload();
}

function toggle_by_id(cls, on) {
    var lst = document.getElementById(cls);
    for(var i = 0; i < lst.length; ++i) {
        lst[i].style.display = on ? '' : 'none';
    }
}


function filterQuestions(){
 	var g = document.getElementById("gender");
 	var gender =  g.options[g.selectedIndex].value;

    var items_lst = ""
    var tbl = document.getElementById('items');
    var rowCount = tbl.rows.length;
    var colCount = 3;

    for (var i = 0;i<rowCount;i++) {
        var myrow = tbl.rows[i];
        var tmp_row = "";
        for (var j=0;j<colCount;j++) {
            if (tmp_row == "") {
                tmp_row = $(myrow.cells[j]).find('select :selected').val()
            } else {
                tmp_row = tmp_row.concat(",").concat($(myrow.cells[j]).find('select :selected').val())
            }
        }
        if (items_lst == "") {
                items_lst = tmp_row
            } else {
                items_lst = items_lst.concat("#").concat(tmp_row)
            }
    }

    post('/filteredresults/', {'gender': gender, 'items_lst': items_lst, csrfmiddlewaretoken: CSRF_TOKEN});

}


function post(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    document.body.appendChild(form);
    form.submit();
}