=====================
Development sketchpad
=====================

Development ideas and work items.

Current
=======

The most important thing at the moment is to implement the basic views.
Full CRUD is not implemented, most things are actually only available
via the admin interface.

Implement asap::

   /                          main view
   /topics/new                create a new topic
   /topics/3/tasks/new        create new task
   /tasks/4/edit              edit task
   /tags                      main tags view

Other to-do items:

-  Document dependencies of INSTALLED_APPS, e.g. the
   ``django.contrib.humanize`` dependency in the templates.

Future plans
============

To-do notes.

-  Learn about HTML 5 and change templates accordingly.
-  Become more proficient with jQuery/JavaScript. It's terrible now.
-  Learn how to write elegant CSS. Is it at all possible? :(

Vague ideas.

-  Calendar widget like on Github that shows when you put in hours.
-  Task types. Book, tutorial, programming project.
