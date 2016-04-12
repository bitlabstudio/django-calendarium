"""Tests for the views of the ``calendarium`` app."""
# ! Never use the timezone now, import calendarium.utils.now instead always
# inaccuracy on microsecond base can negatively influence your tests
# from django.utils.timezone import now
from django.utils.timezone import timedelta
from django.test import TestCase

from django_libs.tests.mixins import ViewRequestFactoryTestMixin
from mixer.backend.django import mixer

from .. import views
from ..models import Event
from ..utils import now


class CalendariumRedirectViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``CalendariumRedirectView`` view."""
    view_class = views.CalendariumRedirectView

    def test_view(self):
        resp = self.client.get(self.get_url())
        self.assertEqual(resp.status_code, 302)


class MonthViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``MonthView`` view class."""
    view_class = views.MonthView

    def get_view_kwargs(self):
        return {'year': self.year, 'month': self.month}

    def setUp(self):
        self.year = now().year
        self.month = now().month

    def test_view(self):
        """Test for the ``MonthView`` view class."""
        # regular call
        resp = self.is_callable()
        self.assertEqual(
            resp.template_name[0], 'calendarium/calendar_month.html', msg=(
                'Returned the wrong template.'))
        self.is_postable(data={'next': True}, to_url_name='calendar_month')
        self.is_postable(data={'previous': True}, to_url_name='calendar_month')
        self.is_postable(data={'today': True}, to_url_name='calendar_month')

        # called with a invalid category pk
        self.is_callable(data={'category': 'abc'})

        # called with a non-existant category pk
        self.is_callable(data={'category': '999'})

        # called with a category pk
        category = mixer.blend('calendarium.EventCategory')
        self.is_callable(data={'category': category.pk})

        # called with wrong values
        self.is_not_callable(kwargs={'year': 2000, 'month': 15})


class WeekViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``WeekView`` view class."""
    view_class = views.WeekView

    def get_view_kwargs(self):
        return {'year': self.year, 'week': self.week}

    def setUp(self):
        self.year = now().year
        # current week number
        self.week = now().date().isocalendar()[1]

    def test_view(self):
        """Tests for the ``WeekView`` view class."""
        resp = self.is_callable()
        self.assertEqual(
            resp.template_name[0], 'calendarium/calendar_week.html', msg=(
                'Returned the wrong template.'))
        self.is_postable(data={'next': True}, to_url_name='calendar_week')
        self.is_postable(data={'previous': True}, to_url_name='calendar_week')
        self.is_postable(data={'today': True}, to_url_name='calendar_week')

        resp = self.is_callable(ajax=True)
        self.assertEqual(
            resp.template_name[0], 'calendarium/partials/calendar_week.html',
            msg=('Returned the wrong template for AJAX request.'))
        self.is_not_callable(kwargs={'year': self.year, 'week': '60'})


class DayViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``DayView`` view class."""
    view_class = views.DayView

    def get_view_kwargs(self):
        return {'year': self.year, 'month': self.month, 'day': self.day}

    def setUp(self):
        self.year = 2001
        self.month = 2
        self.day = 15

    def test_view(self):
        """Tests for the ``DayView`` view class."""
        resp = self.is_callable()
        self.assertEqual(
            resp.template_name[0], 'calendarium/calendar_day.html', msg=(
                'Returned the wrong template.'))
        self.is_postable(data={'next': True}, to_url_name='calendar_day')
        self.is_postable(data={'previous': True}, to_url_name='calendar_day')
        self.is_postable(data={'today': True}, to_url_name='calendar_day')
        self.is_not_callable(kwargs={'year': self.year, 'month': '14',
                                     'day': self.day})


class EventUpdateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``EventUpdateView`` view class."""
    view_class = views.EventUpdateView

    def get_view_kwargs(self):
        return {'pk': self.event.pk}

    def setUp(self):
        self.event = mixer.blend('calendarium.Event')
        self.user = mixer.blend('auth.User', is_superuser=True)

    def test_view(self):
        self.is_callable(user=self.user)


class EventCreateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``EventCreateView`` view class."""
    view_class = views.EventCreateView

    def setUp(self):
        self.user = mixer.blend('auth.User', is_superuser=True)

    def test_view(self):
        self.is_callable(user=self.user)
        self.is_callable(user=self.user, data={'delete': True})
        self.assertEqual(Event.objects.all().count(), 0)


class EventDetailViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``EventDetailView`` view class."""
    view_class = views.EventDetailView

    def get_view_kwargs(self):
        return {'pk': self.event.pk}

    def setUp(self):
        self.event = mixer.blend('calendarium.Event')

    def test_view(self):
        self.is_callable()


class OccurrenceViewTestCaseMixin(object):
    """Mixin to avoid repeating code for the Occurrence views."""
    def get_view_kwargs(self):
        return {
            'pk': self.event.pk,
            'year': self.event.start.date().year,
            'month': self.event.start.date().month,
            'day': self.event.start.date().day,
        }

    def setUp(self):
        self.rule = mixer.blend('calendarium.Rule', name='daily')
        self.event = mixer.blend(
            'calendarium.Event', created_by=mixer.blend('auth.User'),
            start=now() - timedelta(days=1), end=now() + timedelta(days=5),
            rule=self.rule, end_recurring_period=now() + timedelta(days=2))


class OccurrenceDeleteViewTestCase(
        OccurrenceViewTestCaseMixin, ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``OccurrenceDeleteView`` view class."""
    view_class = views.OccurrenceDeleteView

    def test_deletion(self):
        self.is_not_callable(kwargs={
            'pk': 5,
            'year': self.event.start.date().year,
            'month': self.event.start.date().month,
            'day': self.event.start.date().day,
        }, user=self.event.created_by, msg=('Wrong event pk.'))

        self.is_not_callable(kwargs={
            'pk': self.event.pk,
            'year': self.event.start.date().year,
            'month': '999',
            'day': self.event.start.date().day,
        }, user=self.event.created_by, msg=('Wrong dates.'))

        new_rule = mixer.blend('calendarium.Rule', name='weekly',
                               frequency='WEEKLY')
        new_event = mixer.blend(
            'calendarium.Event',
            rule=new_rule,
            end_recurring_period=now() + timedelta(days=200),
            start=now() - timedelta(hours=5),
        )
        test_date = self.event.start.date() - timedelta(days=5)
        self.is_not_callable(kwargs={
            'pk': new_event.pk,
            'year': test_date.year,
            'month': test_date.month,
            'day': test_date.day,
        }, user=self.event.created_by, msg=(
            'No occurrence available for this day.'))

        self.is_callable(user=self.event.created_by)
        self.is_postable(user=self.event.created_by, to='/',
                         data={'decision': 'this one'})


class OccurrenceDetailViewTestCase(
        OccurrenceViewTestCaseMixin, ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``OccurrenceDetailView`` view class."""
    view_class = views.OccurrenceDetailView


class OccurrenceUpdateViewTestCase(
        OccurrenceViewTestCaseMixin, ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``OccurrenceUpdateView`` view class."""
    view_class = views.OccurrenceUpdateView


class UpcomingEventsAjaxViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``UpcomingEventsAjaxView`` view class."""
    view_class = views.UpcomingEventsAjaxView

    def test_view(self):
        self.is_callable()

    def test_view_with_count(self):
        self.is_callable(data={'count': 5})

    def test_view_with_category(self):
        cat = mixer.blend('calendarium.EventCategory')
        self.is_callable(data={'category': cat.slug})
