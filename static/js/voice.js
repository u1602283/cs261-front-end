try {
  var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  var recognition = new SpeechRecognition();
}
catch(e) {
  console.error(e);
}

var noteContent="";
recognition.continuous=true;

recognition.onstart = function() {
  console.log('Voice recognition activated. Try speaking into the microphone.');
}

recognition.onspeechend = function() {
  console.log('You were quiet for a while so voice recognition turned itself off.');
}

recognition.onerror = function(event) {
  if(event.error == 'no-speech') {
    console.log('No speech was detected. Try again.');
  };
}

recognition.onresult = function(event) {

  // event is a SpeechRecognitionEvent object.
  // It holds all the lines we have captured so far.
  // We only need the current one.
  var current = event.resultIndex;

  // Get a transcript of what was said.
  var transcript = event.results[current][0].transcript;

  // Add the current transcript to the contents of our Note.
  noteContent += transcript;
  document.getElementById("inputBox").value = noteContent;
  noteContent="";
}

$('#start-record-btn').on('click', function(e) {
	try{
		recognition.start();
		document.getElementById("start-record-btn").style.backgroundColor = "red";
	}catch (e){
		recognition.stop();
		document.getElementById("start-record-btn").style.backgroundColor = "#32465a";
	}
});
