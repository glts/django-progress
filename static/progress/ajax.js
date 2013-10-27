var csrftoken = $.cookie('csrftoken');

$(function() {
	$('.portion.done').click(function() {
		alert("You've already done this. Good job!! ^__^");
	});
});

$(function() {
	$('.portion.open').click(function() {
		var portion_div = $(this)
		var portion_id = portion_div.find('input').first().val();
		var task_id = portion_div.closest('div.task').find('input').first().val();
		var url = '/progress/tasks/'+task_id+'/portions/'+portion_id+'/close';
		$.ajax(url, {
			type: 'POST',
			crossDomain: false,
			beforeSend: function(jqxhr, settings) {
				jqxhr.setRequestHeader('X-CSRFToken', csrftoken);
			},
		})
		.done(function() {
			portion_div.removeClass('open').addClass('done');
		})
		.fail(function() {
			alert("Ajax request failed");
		});
	});
});
