========
Progress
========

Progress is a simple Django app that helps you keep track of your
progress in current tasks and rewards you with the green tick mark once
you're done. This app is for my own personal use and unfinished.

Prerequisites
=============

*  Python 3.3.x
*  Django 1.5.4
*  South 0.8.2 (probably)
*  Sphinx 1.1.3

I use PostgreSQL with the psycopg driver.

*  psycopg version 2.5.1

Quick start
===========

1. Add "progress" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'progress',
      )

2. Include the progress URLconf in your project urls.py like this::

      url(r'^progress', include('progress.urls')),

3. Run `python manage.py syncdb` to create the progress models.

4. And you're good to go.
