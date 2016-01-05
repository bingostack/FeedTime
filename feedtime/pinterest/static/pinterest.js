
var httpRequest;

document.addEventListener('DOMContentLoaded', function(){
   var source_board = document.getElementById('source');
   makeRequest(source_board);
});

function makeRequest(select) {
	httpRequest = new XMLHttpRequest();
	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}
	httpRequest.onreadystatechange = requestPins;
	var url = '/pinterest/pins?board=' + select.value;
	httpRequest.open('GET', url);
	httpRequest.send(); 
};

function requestPins() {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
			var pin_select = document.getElementById("pinboard");
			pin_select.options.length = 0;
			var json = JSON.parse(httpRequest.responseText); 
			var result = JSON.parse(json.result);
			var data = result.data;
			for(var i=0; i<data.length; i++){
				var id = data[i].id; 
				var note = data[i].note;
				pin_select.options.add(new Option(note, id));   
			}
		} else {
			alert('There was a problem with the request.');
		}
	}
};
