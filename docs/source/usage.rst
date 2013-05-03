Usage
=====

First think about the layout you want to integrate. In most cases you might
want to add the calendar for the current month first. Reverse with::

    {% url "calendar_current_month" %}

Then use the different URLs to let the user navigate through months, weeks and
days. The event management should be intuitive. Be sure to add ``Rule`` models,
if you want to use occurences.

Template Tags
-------------

We provide a template tag to render a defined amount of upcoming occurrences::

    {% render_upcoming_events %}

The default amount is ``5``. You can add your own::

    {% render_upcoming_events 1000 %}
