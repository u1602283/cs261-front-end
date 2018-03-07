$(".messages").animate({scrollTop: $('.messages').get(0).scrollHeight}, "fast");
output = true;

function newMessage(message) {
	message = $(".message-input input").val();
	if($.trim(message) == '') {
		return false;
	}
  //Picture needs changing to something for the user
	$('<li class="sent"><img src="https://cdn.discordapp.com/attachments/400378754427256834/418920166425100299/user.svg" alt="" /><p>' + message + '</p></li>').appendTo($('.messages > ul'));
	$('.message-input input').val(null);
	$(".messages").animate({scrollTop: $('.messages').get(0).scrollHeight}, "fast");
};

function newReply(message) {

	if($.trim(message) == '') {
		return false;
	}
	$('<li class="replies"> <div class="spinner"> <div class="rect1"></div><div class="rect2"></div><div class="rect3"></div><div class="rect4"></div><div class="rect5"></div></div></li>').appendTo($('.messages > ul'));
	//AJAX to server
  fetch('/', {
    method: 'POST',
    body: JSON.stringify({
      type: 'newMessage',
      message: message
    }),
    headers: {
      'content-type': 'application/json'
    }
  })
  .then(response => response.text())
  .then(function(reply) {
		//Add server response
		$('.spinner').remove();
		readOutLoud(reply);
    $('<li class="replies"><img src="https://cdn.discordapp.com/attachments/400378754427256834/418920217104613399/bot.svg" alt="" /><p>' + reply + '</p></li>').appendTo($('.messages > ul'));
    $(".messages").animate({scrollTop: $('.messages').get(0).scrollHeight}, "fast");
  })

}
//Auto call suggest messages
setInterval(suggestMessages, 300000);
function suggestMessages() {

	$('.suggested ul').empty();
  fetch('/', {
    method: 'POST',
    body: JSON.stringify({
      type: 'suggestMessages',
      message: 'message'
    }),
    headers: {
      'content-type': 'application/json'
    }
  }).then(response => response.json())
  .then(function(reply) {
		$('.messages suggested ul').empty();
		console.log(reply);
		for(i = 0; i < reply.length; i++){
			console.log(reply[i])
			$('<li> <p>' + reply[i] + '</p> </li>').appendTo($('.suggested > ul'));
	    $(".messages").animate({scrollTop: $('.messages').get(0).scrollHeight}, "fast");
		}

  })
}


setInterval(getAnomalies, 300000);
function getAnomalies() {
	fetch('/', {
		method: 'POST',
		body: JSON.stringify({
			type: 'detectAnomalies',
			message: 'message'
		}),
		headers: {
			'content-type': 'application/json'
		}
	})
	.then(response => response.json())
	.then(function(reply) {
		array = Array.from(reply);
		clearSnackbar();
		for(i = 0; i < reply.length; i++){
			//message = array[i][1] + "% change for " + array[i][0] + " since market open"
			makeSnackbar(array[i][1], array[i][0]);
		}
		if(reply.length > 0){
			readOutLoud("Anomalies Detected!");
			showSnackbar();
		}
	})

}

$('.suggested ul').on('click','li', function(e) {
  //Send suggested message to api
  message = $(this).text();
	if($.trim(message) == '') {
		return false;
	}
  //Picture needs changing to something for the user
	$('<li class="sent"><img src="https://cdn.discordapp.com/attachments/400378754427256834/418920166425100299/user.svg" alt="" /><p>' + message + '</p></li>').appendTo($('.messages > ul'));
	$('.message-input input').val(null);
	$(".messages").animate({scrollTop: $('.messages').get(0).scrollHeight}, "fast");

  newReply(message);
  suggestMessages();

});

$('.submit').click(function() {
  message = $(".message-input input").val();
  console.log(message);
  newMessage(message);
  newReply(message);
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    message = $(".message-input input").val();
    newMessage(message);
    newReply(message);
    return false;
  }
});
function makeSnackbar(change, code) {
    // Get the snackbar DIV
		$('.popup').append('<li class=\'anomaly_message\' id=' + code + '>' + change + '% change for ' + code + ' since market open' + '</li>');

}

$('.popup').on('click', '.anomaly_message', function(event){
	message = "Get news on " + event.target.id;
	console.log(message);
	$('<li class="sent"><img src="https://cdn.discordapp.com/attachments/400378754427256834/418920166425100299/user.svg" alt="" /><p>' + message + '</p></li>').appendTo($('.messages > ul'));
	newReply(message);
});

function showSnackbar(){
	var x = document.getElementById("snackbar")
	// Add the "show" class to DIV
	x.className = "show";
	// After 3 seconds, remove the show class from DIV
	setTimeout(function(){ x.className = x.className.replace("show", ""); }, 10000);

}
function clearSnackbar(){
	$('.popup').empty();
}
function readOutLoud(message) {
	if(output){
		if(message.length > 240){
			return false;
		}
		var speech = new SpeechSynthesisUtterance();

		// Set the text and voice attributes.
		speech.text = message;
		speech.volume = 1;
		speech.rate = 1;
		speech.pitch = 1;

		window.speechSynthesis.speak(speech);

	}else{
		return false;
	}

}
$('#voice-output-btn').on('click', function(e) {
	if(output){
		output=false;
		document.getElementById("voice-output-btn").style.backgroundColor = "red";
		document.getElementById("voice-output-btn").style.backgroundImage = "url('https://cdn.discordapp.com/attachments/400378754427256834/418937560815894541/sound-off.svg')";

	}else{
		output=true;
		document.getElementById("voice-output-btn").style.backgroundColor = "#32465a";
		document.getElementById("voice-output-btn").style.backgroundImage = "url('https://cdn.discordapp.com/attachments/400378754427256834/418937559305945088/sound-on.svg')";


	}

});
