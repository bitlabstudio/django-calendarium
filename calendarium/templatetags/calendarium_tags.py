"""Templatetags for the ``calendarium`` project."""
from django.core.urlresolvers import reverse
from django import template
from django.utils.timezone import datetime, now, timedelta, utc

from ..models import Event, EventCategory

register = template.Library()


@register.filter
def get_week_URL(date, day=0):
    """
    Returns the week view URL for a given date.

    :param date: A date instance.
    :param day: Day number in a month.

    """
    if day < 1:
        day = 1
    date = datetime(year=date.year, month=date.month, day=day, tzinfo=utc)
    return reverse('calendar_week', kwargs={'year': date.isocalendar()[0],
                                            'week': date.isocalendar()[1]})


@register.inclusion_tag('calendarium/upcoming_events.html')
def render_upcoming_events(event_amount=5, category=None):
    """Template tag to render a list of upcoming events."""
    if not isinstance(category, EventCategory):
        category = None
    return {
        'occurrences': Event.objects.get_occurrences(
            now(),
            now() + timedelta(days=100),
            category,
        )[:event_amount]
    }
