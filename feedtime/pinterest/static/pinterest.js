
var httpRequest;

document.addEventListener('DOMContentLoaded', function()
{
	var source_board = document.getElementById('source');
	requestPins(source_board);
});


function requestPins(control)
{
	var url = '/pinterest/pins?board=' + control.value;
	var callback = function(){onPinsReturned()};
	makeRequest(url, callback);
}


function makeRequest(url, callback) {
	httpRequest = new XMLHttpRequest();
	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}
	httpRequest.onreadystatechange = callback;
	httpRequest.open('GET', url);
	httpRequest.send(); 
};

function onPinsReturned() {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
			var pin_select = document.getElementById("pinboard");
			pin_select.options.length = 0;
			var data = JSON.parse(httpRequest.responseText).result; 
			for(var i=0; i < data.length; i++){
				var id = data[i].id; 
				var note = data[i].note;
				pin_select.options.add(new Option(note, id));   
			}
		} else {
			alert('There was a problem with the request.');
		}
	}
};
