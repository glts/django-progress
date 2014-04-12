var csrftoken = $.cookie('csrftoken');

// TODO File name is misleading this isn't all to do with Ajax

$(function() {
	$('.portion.done').click(function() {
		alert("You've already done this. Good job!! ^__^");
	});
	$('.portion.skipped').click(function() {
		alert("You've already skipped this.");
	});

	// TODO Think about how to select "done" or "skipped" status
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

	$('.submit_effort').click(function() {
		var effort_bar = $(this).closest('div.enter_effort_bar');
		var task_id = $(this).closest('div.task').find('input').first().val();
		var note = $(this).prev().val();
		var url = '/progress/tasks/'+task_id+'/effort_new';
		$.ajax(url, {
			type: 'POST',
			data: {'note': note},
			crossDomain: false,
			beforeSend: function(jqxhr, settings) {
				jqxhr.setRequestHeader('X-CSRFToken', csrftoken);
			},
		})
		.done(function(data) {
			effort_bar.hide();
		})
		.fail(function() {
			alert("Ajax request failed");
		});
	});

	$('.enter_effort_button').click(function() {
		$(this).next().show();
		$(this).hide();
	});
});
