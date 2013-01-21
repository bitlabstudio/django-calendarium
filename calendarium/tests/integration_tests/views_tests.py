"""Tests for the views of the ``calendarium`` app."""
from django.utils.timezone import now
from django.test import TestCase

from django_libs.tests.mixins import ViewTestMixin


class MonthViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``MonthView`` view class."""
    def get_view_name(self):
        return 'calendar_month'

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

        # AJAX call
        resp = self.client.get(
            self.get_url(), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(
            resp.template_name[0], 'calendarium/partials/calendar_month.html',
            msg=('Returned the wrong template for AJAX request.'))

        # called with wrong values
        self.is_not_callable(kwargs={'year': 2000, 'month': 15})


class WeekViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``WeekView`` view class."""
    def get_view_name(self):
        return 'calendar_week'

    def get_view_kwargs(self):
        return {'year': self.year, 'week': self.week}

    def setUp(self):
        self.year = now().year
        # current week number
        self.week = now().date().isocalendar()[1] - 1

    def test_view(self):
        """Tests for the ``WeekView`` view class."""
        resp = self.is_callable()
        self.assertEqual(
            resp.template_name[0], 'calendarium/calendar_week.html', msg=(
                'Returned the wrong template.'))

        resp = self.client.get(
            self.get_url(), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(
            resp.template_name[0], 'calendarium/partials/calendar_week.html',
            msg=('Returned the wrong template for AJAX request.'))
        self.is_not_callable(kwargs={'year': self.year, 'week': '60'})


class DayViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``DayView`` view class."""
    def get_view_name(self):
        return 'calendar_day'

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

        resp = self.client.get(
            self.get_url(), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(
            resp.template_name[0], 'calendarium/partials/calendar_day.html',
            msg=('Returned the wrong template for AJAX request.'))
        self.is_not_callable(kwargs={'year': self.year, 'month': '14',
                                     'day': self.day})
