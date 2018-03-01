$(".messages").animate({scrollTop: $('.messages').get(0).scrollHeight}, "fast");

function newMessage(message) {
	message = $(".message-input input").val();
	if($.trim(message) == '') {
		return false;
	}
  //Picture needs changing to something for the user
	$('<li class="sent"><img src="https://i.imgur.com/z12PaJ6.png" alt="" /><p>' + message + '</p></li>').appendTo($('.messages > ul'));
	$('.message-input input').val(null);
	$(".messages").animate({scrollTop: $('.messages').get(0).scrollHeight}, "fast");
};

function newReply(message) {

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
    $('<li class="replies"><img src="https://www.seoclerk.com/pics/want52167-1vt94o1498116476.png" alt="" /><p>' + reply + '</p></li>').appendTo($('.messages > ul'));
    $(".messages").animate({scrollTop: $('.messages').get(0).scrollHeight}, "fast");
  })

}
//Auto call suggest messages
setInterval(suggestMessages, 3000000);
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


setInterval(getAnomalies, 15000);
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
		Array.from(reply);
		console.log(reply);
		$('<li class="replies"><img src="https://www.seoclerk.com/pics/want52167-1vt94o1498116476.png" alt="" /><p>' + reply + '</p></li>').appendTo($('.messages > ul'));
    $(".messages").animate({scrollTop: $('.messages').get(0).scrollHeight}, "fast");
	})

}

$('.suggested ul').on('click','li', function(e) {
  //Send suggested message to api
  message = $(this).text();
	if($.trim(message) == '') {
		return false;
	}
  //Picture needs changing to something for the user
	$('<li class="sent"><img src="https://i.imgur.com/z12PaJ6.png" alt="" /><p>' + message + '</p></li>').appendTo($('.messages > ul'));
	$('.message-input input').val(null);
	$(".messages").animate({scrollTop: $('.messages').get(0).scrollHeight}, "fast");

  newReply(message);
  suggestMessages();

});

$('.submit').click(function() {
  message = $(".message-input input").val();
  console.log(message)
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
