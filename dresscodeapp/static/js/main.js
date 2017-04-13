function postAnswer(questionId, vote, userScore){
	// add loading animation to button
	//$('#pic'+questionId).hide()
	//$('#yay'+questionId).hide()
	//$('#meh'+questionId).hide()
	//$('#nay'+questionId).hide()
	$('#thanks'+questionId).show()
	$('#question'+questionId).hide()
	$('#thanks'+questionId).fadeOut(1000)
	var numOfVisibleRows = $('tr:visible')
	var thankyou = 'Thanks for answering!';
	var text = userScore > 10 ? '\nYou have enough credit. Post!' : 'Only '+ (10 - userScore) + ' to go';
	$('#msgText'+questionId).text(thankyou+text + numOfVisibleRows);
	$.ajax({
				url: "/post-answer/",
				type: 'POST',
				data: {
					'question_id': questionId,
					'vote': vote,
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

function toggle_by_id(cls, on) {
    var lst = document.getElementById(cls);
    for(var i = 0; i < lst.length; ++i) {
        lst[i].style.display = on ? '' : 'none';
    }
}