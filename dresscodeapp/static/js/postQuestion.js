function postQuestion(){
    var e = document.getElementById("title")
    var title =  e.options[e.selectedIndex].value;
    if (!validateTitle(title)) {
        return
    }
    var description =  document.getElementById("comment").value;

    var date=$("#date").val();
    if (!validateDate(date)) {
        return
    }

    var photo = document.getElementById("pic").files[0];
    if (!validateFile(photo)) {
        return
    }

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

    if (!validateItems(items_lst)) {
        return
    }

    var data = new FormData();
    data.append('photos', photo)
    data.append('title', title)
    data.append('description', description)
    data.append('date', date)
    data.append('items_lst', items_lst)
    data.append('csrfmiddlewaretoken', CSRF_TOKEN)

    $.ajax({
				url: "/post-question/",
				type: 'POST',
				method: 'POST',
				data: data,
				contentType: false,
                processData: false,
			success: function(response) {
  				result = JSON.parse(response);  // Get the results sended from ajax to here
  				if (result.error) {
      				// Error
      				alert(result.error_text);
  				} else {
              		alert("Your question was posted successfully!\nLet's answer other users questions!")
              		window.location.replace("/questionsfeed/");
      			}
  			}
		});
}

var numOfItems = 0
function addClothingItemRow() {
    numOfItems = numOfItems+1
    $('#items').find('tbody').append('<tr><td class="col-md-2"><select class="form-control"><option value="" selected disabled>Item</option><option>T-Shirt</option><option>Shirt</option><option>Hoodie</option><option>Suit</option><option>Short Pants</option><option>Jeans</option><option>Pants</option><option>Dress</option><option>Skirt</option><option>Shoes</option><option>Swim Suit</option><option>Hat</option></select></td><td class="col-md-2"><select class="form-control"><option value="" selected disabled>Color</option><option>Blue</option><option>Red</option><option>Black</option><option>White</option><option>Purple</option><option>Green</option><option>Yellow</option><option>Brown</option><option>Grey</option></select></td><td class="col-md-2"><select class="form-control"><option value="" selected disabled>Pattern</option><option>None</option><option>Stripes</option><option>Dots</option><option>Checked</option></select></td><td class="col-md-2"><button class="btn btn" type="button" onclick="addClothingItemRow()"><span class="glyphicon glyphicon-plus"></span></button> <button class="btn btn" type="button" onclick="removeClothingItemRow(this)"><span class="glyphicon glyphicon-minus"></span></button></td></tr>');
}

function removeClothingItemRow(e){
    if (numOfItems > 0) {
        numOfItems = numOfItems-1
        e.parentNode.parentNode.parentNode.removeChild(e.parentNode.parentNode);
    }
}

function validateTitle(title) {
    if (title=="") {
        alert("Please select event from list")
        return false
    }
    return true
}

function validateDate(date) {
    if (date=="") {
        alert("Please select due date for your question")
        return false
    }
    var parts = date.split('/');
    //please put attention to the month (parts[0]), Javascript counts months from 0:
    // January - 0, February - 1, etc
    var mydate = new Date(parts[2],parts[0]-1,parts[1],'23','59','59');
    var today = new Date()
    if (mydate < today) {
        alert("Please select future due date")
        return false
    }
    return true
}

function validateFile(file) {
    if (typeof file == 'undefined' ) {
        alert("Please upload a photo of your look")
        return false;
    }
    var valid = false
    var sFileName = file.name
    var _validFileExtensions = [".jpg", ".jpeg", ".bmp", ".gif", ".png"];
        for (var j = 0; j < _validFileExtensions.length; j++) {
            var sCurExtension = _validFileExtensions[j];
            if (sFileName.substr(sFileName.length - sCurExtension.length, sCurExtension.length).toLowerCase() == sCurExtension.toLowerCase()) {
                valid = true;
                break;
            }
    }
    if (!valid) {
        alert("The file was uploaded is not a photo, please upload a file from type: .jpg, .jpeg, .bmp, .gif, .png")
        return false
    }
    return true;
}

function validateItems(items_lst) {
    if (items_lst == "") {
        alert("Please specify the clothing items of your look")
        return false
    }
    var lines = items_lst.split("#");
    for (var j = 0; j < lines.length; j++) {
        if (lines[j] == "") {
            continue
        }
        var sub_items = lines[j].split(",")
        if (sub_items[0] == "") {
            alert("Please specify clothing items in row " + (j+1))
            return false
        }
        if (sub_items[1] == "") {
            alert("Please specify color fot item " + sub_items[0])
            return false
        }

        if (sub_items[2] == "") {
            alert("Please specify pattern fot item " + sub_items[0])
            return false
        }

    }
    return true
}
