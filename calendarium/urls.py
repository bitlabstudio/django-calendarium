"""URLs for the ``calendarium`` app."""
from django.conf.urls.defaults import patterns, url

from calendarium.views import (
    DayView,
    EventCreateView,
    EventDeleteView,
    EventDetailView,
    EventUpdateView,
    MonthView,
    WeekView,
)


urlpatterns = patterns(
    '',
    # event views
    url(r'^event/create/$',
        EventCreateView.as_view(),
        name='calendar_event_create'),

    url(r'^event/(?P<pk>\d+)/$',
        EventDetailView.as_view(),
        name='calendar_event_detail'),

    url(r'^event/(?P<pk>\d+)/update/$',
        EventUpdateView.as_view(),
        name='calendar_event_update'),

    url(r'^event/(?P<pk>\d+)/delete/$',
        EventDeleteView.as_view(),
        name='calendar_event_delete'),

    # calendar views
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$',
        MonthView.as_view(),
        name='calendar_month'),

    url(r'^(?P<year>\d+)/week/(?P<week>\d+)/$',
        WeekView.as_view(),
        name='calendar_week'),

    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
        DayView.as_view(),
        name='calendar_day'),
)
