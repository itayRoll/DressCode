var numOfCalls = 0
var userScoreGlobal = -1

function sendNegativeReport(qpk, numOfQuestions) {
  $.ajax({
        url: "/negative-report/",
        type: 'POST',
        data: {
          'qpk': qpk,
          csrfmiddlewaretoken: CSRF_TOKEN,
        },
      success: function(response) {
          if (response.localeCompare("true") == 0) {
            // thanks for your feedback
            alert("thanks for your feedback");
            postAnswer(qpk, -1, numOfQuestions, -1)
          } else {
            alert("you already voted, we're looking into it");
          }
        }
    });
}

function postPreAnswer(questionId, vote, numOfQuestions) {
    postAnswer(questionId, vote, numOfQuestions, -1)
}

function postAnswer(questionId, vote, numOfQuestions, userScore) {
  // by counting number of calls we can know how many answers user have answers so far,
  // and know when loaded feed is done, and more feed should be loaded.
  numOfCalls = numOfCalls+1
  if (vote >=0) { // vote = -1 when user report negative report
        $('#thanks'+questionId).show()
        $('#thanks'+questionId).fadeOut(5000)
        var thankyou = 'Thanks for answering!';
        var text="";
        if (userScore >= 0) {
            if (userScoreGlobal < 0) {
                userScoreGlobal = userScore;
            }
            userScoreGlobal++;
            text = userScoreGlobal >= 10 ? '\nYou have enough credit. Post!' : '\nOnly '+ (10 - userScoreGlobal) + ' to go';
        }
        $('#msgText'+questionId).text(thankyou+text);
    }
    $('#question'+questionId).hide()
    $('#question_row'+questionId).fadeOut(5000)
	if (numOfCalls == numOfQuestions)  // load more feed!!
	{
	    $('#questions_table').hide()
	    $('#gettoknowyou').hide()
	    $('#divreload').show()
	    setTimeout(function(){ window.location.href = '../questionsfeed/'; }, 4000);
	}
	if (vote >= 0) {
        $.ajax({
                    url: "/post-answer/",
                    type: 'POST',
                    data: {
                        'question_id': questionId,
                        'vote': vote,
                        csrfmiddlewaretoken: CSRF_TOKEN,
                    },
                success: function(response) {
                    var s = response
                    if (s.startsWith("spam")){
                        username = s.split("#")[1]
                        // alert spammer before ban
                        var modal = document.getElementById('modal-spam');
                        modal.style.display='block'
                        modal.innerHTML = modal.innerHTML.replace("username", username)
                    }
                }
            });
	}
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

function viewResults(questionId){
	$.ajax({
				url: "/view-result/",
				type: 'POST',
				data: {
					'question_id': questionId,
					csrfmiddlewaretoken: CSRF_TOKEN,
				},
			success: function(response) {
  				result = JSON.parse(response);  // Get the results sended from ajax to here
  				if (result.error) {
      				// Error
      				alert(result.error_text);
  				} else {
              		window.location.replace("/question-result/"+result["q_id"]);
      			}
  			}
		});
}

function filterResults(questionId){
    var e = document.getElementById('gender')
    var gender = e.options[e.selectedIndex].value;
    if (gender == "") {
        gender = "u"
    }

    e = document.getElementById('minAge')
    var min = e.options[e.selectedIndex].value;
    if (min == "") {
        min = "0"
    }

     e = document.getElementById('maxAge')
    var max = e.options[e.selectedIndex].value;
    if (max == "") {
        max = "0"
    }

  	$.ajax({
  				url: "/view-result/",
  				type: 'POST',
  				data: {
  				    'minAge': min,
  				    'maxAge': max,
  				    'gender':gender,
  					'question_id': questionId,
  					csrfmiddlewaretoken: CSRF_TOKEN,
  				},
  			success: function(response) {
    				result = JSON.parse(response);  // Get the results sended from ajax to here
    				if (result.error) {
        				// Error
        				alert(result.error_text);
    				} else {
                		window.location.replace("/view-result-filter/"+result["q_id"]+"/"+result["gender"]+"/"+result["minAge"]+"/"+result["maxAge"]+"/");
        			}
    			}
  		});
}

function checkPasswordMatch() {
    // verify that user has entered the same password in both fields
    var password = $("#password").val();
    var confirmPassword = $("#confirm_password").val();

    if (password != confirmPassword){
        document.getElementById("confirm_password").style.borderColor = "red";
        document.getElementById("signUpBtn").disabled = true;
    } else {
        document.getElementById('confirm_password').style.removeProperty('border');
        document.getElementById("signUpBtn").disabled = false;
    }
}