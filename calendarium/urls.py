"""URLs for the ``calendarium`` app."""
from django.conf.urls import url

from . import views


urlpatterns = [
    # event views
    url(r'^event/create/$',
        views.EventCreateView.as_view(),
        name='calendar_event_create'),

    url(r'^event/(?P<pk>\d+)/$',
        views.EventDetailView.as_view(),
        name='calendar_event_detail'),

    url(r'^event/(?P<pk>\d+)/update/$',
        views.EventUpdateView.as_view(),
        name='calendar_event_update'),

    url(r'^event/(?P<pk>\d+)/delete/$',
        views.EventDeleteView.as_view(),
        name='calendar_event_delete'),

    # occurrence views
    url(r'^event/(?P<pk>\d+)/date/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
        views.OccurrenceDetailView.as_view(),
        name='calendar_occurrence_detail'),

    url(
        r'^event/(?P<pk>\d+)/date/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/update/$',  # NOPEP8
        views.OccurrenceUpdateView.as_view(),
        name='calendar_occurrence_update'),

    url(
        r'^event/(?P<pk>\d+)/date/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/delete/$',  # NOPEP8
        views.OccurrenceDeleteView.as_view(),
        name='calendar_occurrence_delete'),

    # calendar views
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$',
        views.MonthView.as_view(),
        name='calendar_month'),

    url(r'^(?P<year>\d+)/week/(?P<week>\d+)/$',
        views.WeekView.as_view(),
        name='calendar_week'),

    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
        views.DayView.as_view(),
        name='calendar_day'),

    url(r'^get-events/$',
        views.UpcomingEventsAjaxView.as_view(),
        name='calendar_upcoming_events'),

    url(r'^$',
        views.CalendariumRedirectView.as_view(),
        name='calendar_current_month'),

]
