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
  //Need to put in the message reply here
  // var response = new XMLHttpRequest();
  // response.open('POST', 'http://localhost:8080');
  // response.onreadystatechange = function() {
  //   if(response.readystate === 4) {
  //     $('<li class="replies"><img src="https://www.seoclerk.com/pics/want52167-1vt94o1498116476.png" alt="" /><p>' + request.responseText + '</p></li>').appendTo($('.messages ul'));
  //     $(".messages").animate({ scrollTop: $(document).height() }, "fast");
  //   }
  // }
  // console.log("Request Prepped");
  // response.send(message);
  // console.log("Request Sent");
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
    $('<li class="replies"><img src="https://www.seoclerk.com/pics/want52167-1vt94o1498116476.png" alt="" /><p>' + reply + '</p></li>').appendTo($('.messages > ul'));
    $(".messages").animate({ scrollTop: $(document).height() }, "fast");
  })

}
//Auto call suggest messages
setInterval(suggestMessages, 150000);
function suggestMessages() {
  //Clear previous suggested messages
  //Pull array of suggested messages and add them
  // var response = new XMLHttpRequest();
  // response.open('POST', 'http://localhost:8080');
  // response.onreadystatechange = function() {
  //   if(response.readystate === 4) {
  //     $('.messages suggested').val(null)
  //     $('<li class="suggested">' + request.responseText + '</li>').appendTo($('.messages ul'));
  //   }
  // }
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
    // $('<li class="replies"><img src="https://www.seoclerk.com/pics/want52167-1vt94o1498116476.png" alt="" /><p>' + reply + '</p></li>').appendTo($('.messages ul'));
    // $(".messages").animate({ scrollTop: $(document).height() }, "fast");
  })
}

$('.suggest').click(function() {
  //Send suggested message to api
  //Print response
  newReply();
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
