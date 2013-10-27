=====
Intro
=====

Progress is a tiny Django app that helps track progress over
user-defined tasks.

I'm working on this for myself, the prime motivators being a) make a
tool to help me stay motivated, and b) learn Django and polish my
amateur web dev skills.

What does it do
===============

You define *topics* that you are working on.

Then you define *tasks*, any number of tasks that you want to work on
under that topic header. A task can be one of two kinds:

-  A *challenge*, a discrete task that has a start and an end, and
   can be subdivided into work portions. Once all are done, the challenge
   is finished.
-  A *routine*, a long-term, ongoing task, that you want to keep working
   on but that doesn't have discrete work portions, and that doesn't
   have a well-defined end.

A challenge could be a book that you want to read, or a tutorial for a
programming language that you want to work through.

A routine could be practicing an instrument, or doing work on some
open-ended personal project.

How do I use it
===============

Set the whole thing up, then start creating these items, mostly via the
admin view, since I haven't implemented all CRUD operations yet.

Nice thing is, you can click on portions to make them green. And in the
end the task gets a tick mark. Yes a tickmark :D
