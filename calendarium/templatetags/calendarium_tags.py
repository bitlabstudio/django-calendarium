"""Templatetags for the ``calendarium`` project."""
from django.core.urlresolvers import reverse
from django import template
from django.utils.timezone import datetime, utc

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
