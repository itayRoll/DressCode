function postAnswer(questionId, vote, userScore){
	// add loading animation to button
	$('#yay'+questionId).hide()
	$('#nay'+questionId).hide()
	$('#msg'+questionId).show()
	var text = userScore > 10 ? 'You have enough credit. Post!' : 'Only '+ (10 - userScore) + ' to go';
	$('#msgText'+questionId).text(text);
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