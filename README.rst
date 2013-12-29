Django Calendarium
==================

A Django application for managing and displaying a calendar and it's events
in your templates.

It will be heavily influenced by the awesome
`django-schedule <https://github.com/thauber/django-schedule>`_

Since that project is unfortunately no longer maintained, we will try to revive
it's ideas with TDD, class based views and AJAX in mind.

For further information, please check out the 
`django-calendarium documentation <https://django-calendarium.readthedocs.org/>`_
on readthedocs.


Settings
--------

If you want your calendar to start on a different date, you can set the
``CALENDARIUM_SHIFT_WEEKSTART`` setting to be the offset in days, that the
calendar should add or subtract from the start day of the week. Most common
case is probably, that you want your calendar week to start on sunday in which
case you would add the following to your settings::

.. code-block:: python

    CALENDARIUM_SHIFT_WEEKSTART = -1


Extending the app
-----------------

It is almost inevitable that you will want to add more fields or more
functionality to the Event model of this app. However, this app is already
quite complex and we would like to keep it as simple and focused as possible.
This app should do one thing and do it well, and that thing is: to output
(recurring) events for a given day, week, month or timeframe.

A very common usecase is to display public events that are open for
registration. For this case we have created another app `django-event-rsvp
<https://github.com/bitmazk/django-event-rsvp>`_ which plays nicely with this
app.

You might do it in a similar way. Since events created in the calendarium app
can easily be tied to any object via generic foreign keys, you can therefore
tie them to the objects of any of your own apps. The only thing left for you is
to create nice CRUD views that create your own objects and our Event objects
simultaneously behind the scenes.


Roadmap
-------

Check the issue tracker on github for milestones and features to come. If you
have ideas or questions, please don't hesitate to open an issue on the issue
tracker.
