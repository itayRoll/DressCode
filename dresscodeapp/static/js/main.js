function postAnswer(questionId, vote, userScore){
	// add loading animation to button
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

function addClothingItemRow() {
	$('#clothing-items').append('<br><div class="row"><div class="col-md-2"><div class="dropdown"><button class="btn dropdown-toggle" type="button" data-toggle="dropdown">Item<span class="caret"></span></button><ul class="dropdown-menu"><li><a href="#">T-Shirt</a></li><li><a href="#">Shirt</a></li><li><a href="#">Hoodie</a></li><li><a href="#">Hoodie</a></li><li><a href="#">Suit</a></li><li><a href="#">Short Pants</a></li><li><a href="#">Jeans</a></li><li><a href="#">Pants</a></li><li><a href="#">Dress</a></li><li><a href="#">Skirt</a></li><li><a href="#">Shoes</a></li><li><a href="#">Swim Suit</a></li><li><a href="#">Hat</a></li></ul></div></div><div class="col-md-2"><div class="dropdown"><button class="btn dropdown-toggle" type="button" data-toggle="dropdown">Color<span class="caret"></span></button><ul class="dropdown-menu"><li><a href="#">Blue</a></li><li><a href="#">Red</a></li><li><a href="#">Black</a></li><li><a href="#">White</a></li><li><a href="#">Purple</a></li><li><a href="#">Green</a></li><li><a href="#">Yellow</a></li><li><a href="#">Brown</a></li><li><a href="#">Grey</a></li></ul></div></div><div class="col-md-2"><div class="dropdown"><button class="btn dropdown-toggle" type="button" data-toggle="dropdown">Pattern<span class="caret"></span></button><ul class="dropdown-menu"><li><a href="#">None</a></li><li><a href="#">Stripes</a></li><li><a href="#">Dots</a></li><li><a href="#">Checked</a></li></ul></div></div><div class="col-md-2"><button class="btn btn-warning" type="button" onclick="addClothingItemRow()"><span class="glyphicon glyphicon-plus"></span></button></div></div>');
}

function toggle_by_id(cls, on) {
    var lst = document.getElementById(cls);
    for(var i = 0; i < lst.length; ++i) {
        lst[i].style.display = on ? '' : 'none';
    }
}