var numOfCalls = 0
function postAnswer(questionId, vote, userScore){
    numOfCalls = numOfCalls+1
	// add loading animation to button
	$('#thanks'+questionId).show()
	$('#question'+questionId).hide()
    var itemsNotAsPic = true
	if ($('#checkbox'+questionId).checked) {
        itemsNotAsPic = false
        alert("checked");
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

function postQuestion(){
    var photo_path = document.getElementById("pic").value;
    var photo = document.getElementById("pic").files; // somehow upload the photo to the server....
    var e = document.getElementById("title")
    var title =  e.options[e.selectedIndex].value;
    var description =  document.getElementById("comment").value;
    var date=$("#date").val();

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

    $.ajax({
				url: "/post-question/",
				type: 'POST',
				method: 'POST',
				data: {
					'title': title,
					'path': photo_path,
					'description': description,
					'date': date,
					'items_lst': items_lst,
					csrfmiddlewaretoken: CSRF_TOKEN
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

var numOfItems = 0
function addClothingItemRow() {
    numOfItems = numOfItems+1
    $('#items').find('tbody').append('<tr><td class="col-md-2"><select class="form-control"><option value="" selected disabled>Item</option><option>T-Shirt</option><option>Shirt</option><option>Hoodie</option><option>Hoodie</option><option>Suit</option><option>Short Pants</option><option>Jeans</option><option>Pants</option><option>Dress</option><option>Skirt</option><option>Shoes</option><option>Swim Suit</option><option>Hat</option></select></td><td class="col-md-2"><select class="form-control"><option value="" selected disabled>Color</option><option>Blue</option><option>Red</option><option>Black</option><option>White</option><option>Purple</option><option>Green</option><option>Yellow</option><option>Brown</option><option>Grey</option></select></td><td class="col-md-2"><select class="form-control"><option value="" selected disabled>Pattern</option><option>None</option><option>Stripes</option><option>Dots</option><option>Checked</option></select></td><td class="col-md-2"><button class="btn btn-warning" type="button" onclick="addClothingItemRow()"><span class="glyphicon glyphicon-plus"></span></button></td><td class="col-md-2"><button class="btn btn-warning" type="button" onclick="removeClothingItemRow(this)"><span class="glyphicon glyphicon-minus"></span></button></td></tr>');
    //$('#clothing-items').append('<tr><td class="col-md-2"><select class="form-control"><option value="" selected disabled>Item</option><option>T-Shirt</option><option>Shirt</option><option>Hoodie</option><option>Hoodie</option><option>Suit</option><option>Short Pants</option><option>Jeans</option><option>Pants</option><option>Dress</option><option>Skirt</option><option>Shoes</option><option>Swim Suit</option><option>Hat</option></select></td><td class="col-md-2"><select class="form-control"><option value="" selected disabled>Color</option><option>Blue</option><option>Red</option><option>Black</option><option>White</option><option>Purple</option><option>Green</option><option>Yellow</option><option>Brown</option><option>Grey</option></select></td><td class="col-md-2"><select class="form-control"><option value="" selected disabled>Pattern</option><option>None</option><option>Stripes</option><option>Dots</option><option>Checked</option></select></td><td class="col-md-2"><button class="btn btn-warning" type="button" onclick="addClothingItemRow()"><span class="glyphicon glyphicon-plus"></span></button></td><td class="col-md-2"><button class="btn btn-warning" type="button" onclick="removeClothingItemRow(this)"><span class="glyphicon glyphicon-minus"></span></button></td></tr>');
	$('#output').text(numOfItems)
}

function removeClothingItemRow(e){
    if (numOfItems > 0) {
        numOfItems = numOfItems-1
        e.parentNode.parentNode.parentNode.removeChild(e.parentNode.parentNode);
    }
}

function toggle_by_id(cls, on) {
    var lst = document.getElementById(cls);
    for(var i = 0; i < lst.length; ++i) {
        lst[i].style.display = on ? '' : 'none';
    }
}