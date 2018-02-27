$(".messages").animate({ scrollTop: $(document).height() }, "fast");

function newMessage(message) {
	message = $(".message-input input").val();
	if($.trim(message) == '') {
		return false;
	}
  //Picture needs changing to something for the user
	$('<li class="sent"><img src="http://emilcarlsson.se/assets/mikeross.png" alt="" /><p>' + message + '</p></li>').appendTo($('.messages > ul'));
	$('.message-input input').val(null);
	$(".messages").animate({ scrollTop: $(document).height() }, "fast");
};

function newReply(message) {
  console.log(message);
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
    $('<li class="replies"><img src="https://www.seoclerk.com/pics/want52167-1vt94o1498116476.png" alt="" /><p>' + reply + '</p></li>').appendTo($('.messages > ul'));
    $(".messages").animate({ scrollTop: $(document).height() }, "fast");
  })

}
//Auto call suggest messages
setInterval(suggestMessages, 15000000);
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
  })
  .then(response => response.text())
  .then(function(reply) {
    $('<li><p>' + reply + '</p></li>').appendTo($('.messages suggested ul'));
    $(".messages").animate({ scrollTop: $(document).height() }, "fast");
  })
}

setInterval(getAnomalies, 15000000);
function getAnomalies() {
	fetch('/', {
		method: 'POST',
		body: JSON.stringify({
			type: 'anomalies',
			message: 'message'
		}),
		headers: {
			'content-type': 'application/json'
		}
	})
	.then(response => response.text())
	.then(function(reply) {
		$('<li class="replies"><img src="https://www.seoclerk.com/pics/want52167-1vt94o1498116476.png" alt="" /><p>' + reply + '</p></li>').appendTo($('.messages > ul'));
    $(".messages").animate({ scrollTop: $(document).height() }, "fast");
	})

}

$('.suggested ul li').click(function(e) {
  //Send suggested message to api
  message = $(this).text();
	if($.trim(message) == '') {
		return false;
	}
  //Picture needs changing to something for the user
	$('<li class="sent"><img src="http://emilcarlsson.se/assets/mikeross.png" alt="" /><p>' + message + '</p></li>').appendTo($('.messages > ul'));
	$('.message-input input').val(null);
	$(".messages").animate({ scrollTop: $(document).height() }, "fast");

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
