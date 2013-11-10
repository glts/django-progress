var csrftoken = $.cookie('csrftoken');

$(function() {
	$('.portion.done').click(function() {
		alert("You've already done this. Good job!! ^__^");
	});

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
		.done(function(data) {
			portion_div.removeClass('open').addClass('done');
			if (data.challenge.done) {
				portion_div.closest('div.task').addClass('done');
			}
		})
		.fail(function() {
			alert("Ajax request failed");
		});
	});

	$('.touch_button').click(function() {
		var task_id = $(this).closest('div.task').find('input').first().val();
		var url = '/progress/tasks/'+task_id+'/touch';
		$.ajax(url, {
			type: 'POST',
			crossDomain: false,
			beforeSend: function(jqxhr, settings) {
				jqxhr.setRequestHeader('X-CSRFToken', csrftoken);
			},
		})
		.done(function(data) {
			console.log(data);  // TODO
		})
		.fail(function() {
			alert("Ajax request failed");
		});
	});
});
