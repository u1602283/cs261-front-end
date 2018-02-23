<script >$(".messages").animate({ scrollTop: $(document).height() }, "fast");

function newMessage() {
	message = $(".message-input input").val();
	if($.trim(message) == '') {
		return false;
	}
  //Picture needs changing to something for the user
	$('<li class="sent"><img src="http://emilcarlsson.se/assets/mikeross.png" alt="" /><p>' + message + '</p></li>').appendTo($('.messages ul'));
	$('.message-input input').val(null);
	$(".messages").animate({ scrollTop: $(document).height() }, "fast");
};

function newReply() {
  //Need to put in the message reply here
  message = "";
  $('<li class="replies"><img src="https://www.seoclerk.com/pics/want52167-1vt94o1498116476.png" alt="" /><p>' + message + '</p></li>').appendTo($('.messages ul'));
	$('.message-input input').val(null);
	$(".messages").animate({ scrollTop: $(document).height() }, "fast");

}
function suggestMessages() {
  //Clear previous suggested messages
  //Pull array of suggested messages and add them
}

$('.suggest').click(function() {
  //Send suggested message to api
  //Print response
  newReply();
});

$('.submit').click(function() {
  newMessage();
  newReply();
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    newMessage();
    return false;
  }
});
