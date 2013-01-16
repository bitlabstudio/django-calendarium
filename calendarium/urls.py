"""URLs for the ``calendarium`` app."""
from django.conf.urls.defaults import patterns, url

from calendarium.views import DayView, MonthView, WeekView


urlpatterns = patterns(
    '',
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$',
        MonthView.as_view(),
        name='calendar_month',
    ),

    url(r'^(?P<year>\d+)/week/(?P<week>\d+)/$',
        WeekView.as_view(),
        name='calendar_week',
    ),

    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
        DayView.as_view(),
        name='calendar_day',
    ),

)
