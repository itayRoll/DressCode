function postQuestion(){
    var e = document.getElementById("title")
    var title =  e.options[e.selectedIndex].value;
    if (!validateTitle(title)) {
        return false;  
    }
    var description =  document.getElementById("comment").value;

    var date=$("#date").val();
    if (!validateDate(date)) {
        return false;
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
        return false;
    }

    var photo = document.getElementById("pic").files[0];
    if (!validateFile(photo)) {
        return false;
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
              		window.location.replace("/question-result/" + result.qpk +"/");
      			}
  			}
		});
    //alert("waiting...");
}

var numOfItems = 0
function addClothingItemRow() {
    numOfItems = numOfItems+1
    $('#items').find('tbody').append('<tr><td class="col-md-2"><select class="form-control" required><option value="" selected disabled>Item</option><option value="1">T-Shirt</option><option value="2">Shirt</option><option value="6">Hoodie</option><option value="10">Suit</option><option value="3">Short Pants</option><option value="13">Jeans</option><option value="11">Pants</option><option value="7">Dress</option><option value="12">Skirt</option><option value="5">Shoes</option><option value="9">Swim Suit</option><option value="4">Hat</option><option value="14">Tie</option><option value="15">Scarf</option><option value="16">Jacket</option></select></td><td class="col-md-2"><select class="form-control" required><option value="" selected disabled>Color</option><option value="1">Blue</option><option value="2">Red</option><option value="3">Black</option><option value="4">White</option><option value="5">Purple</option><option value="6">Green</option><option value="7">Yellow</option><option value="8">Brown</option><option value="9">Grey</option></select></td><td class="col-md-2"><select class="form-control" required><option value="" selected disabled>Pattern</option><option value="1">None</option><option value="2">Stripes</option><option value="3">Dots</option><option value="4">Checked</option></select></td><td class="col-md-2"><button class="btn btn" type="button" onclick="addClothingItemRow()"><span class="glyphicon glyphicon-plus"></span></button> <button class="btn btn" type="button" onclick="removeClothingItemRow(this)"><span class="glyphicon glyphicon-minus"></span></button></td></tr>');
}

function removeClothingItemRow(e){
    if (numOfItems > 0) {
        numOfItems = numOfItems-1
        e.parentNode.parentNode.parentNode.removeChild(e.parentNode.parentNode);
    }
}

function validateTitle(title) {
    if (title=="") {
        //alert("Please select event from list")
        return false
    }
    return true
}

function validateDate(date) {
    if (date=="") {
        //alert("Please select due date for your question")
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
        return false;
    }
    var lines = items_lst.split("#");
    for (var j = 0; j < lines.length; j++) {
        if (lines[j] == "") {
            //alert("Please fill clothing item " + (j+1) + " or remove it.");
            return false;
            // continue;
        }
        var sub_items = lines[j].split(",");
        if (sub_items[0] == "") {
            //alert("Please specify clothing items in row " + (j+1))
            return false;
        }
        if (sub_items[1] == "") {
            //alert("Please specify color fot item " + sub_items[0])
            return false;
        }

        if (sub_items[2] == "") {
            //alert("Please specify pattern fot item " + sub_items[0])
            return false;
        }

    }
    return true
}
