var httpRequest;

document.addEventListener('DOMContentLoaded', function() {
	var source_board = document.getElementById('source');
	requestPins(source_board);
});

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

function onPinsReturned() 
{
	if (httpRequest.readyState === XMLHttpRequest.DONE) 
    {
		if (httpRequest.status === 200) 
        {
			var pin_select = document.getElementById("pinboard");
			pin_select.options.length = 0;
			var data = JSON.parse(httpRequest.responseText).result; 
			for (var i=0; i < data.length; i++) {
				var id = data[i].id;
				var note = data[i].note;
				pin_select.options.add(new Option(note, id));   
			}
            getPinData();
		} else { alert('There was a problem with the request.'); }
	}
};

function onUrlReturned()
{
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
			var pin_img = document.getElementById("pin_img");
			var json = JSON.parse(httpRequest.responseText).result;
            pin_img.src = json['image']['original']['url']
            var note = document.getElementById("pin_note");
            note.value = json["note"] 
			var link = document.getElementById("pin_link");
			pin_link.value = json['original_link'];
		} else { alert('There was a problem with the request.'); }
    }
};
