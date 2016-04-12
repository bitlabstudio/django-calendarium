"""Tests for the template tags of the ``calendarium`` app."""
from django.template import Context, Template
from django.test import TestCase
from django.utils import timezone

from mixer.backend.django import mixer

from ..templatetags.calendarium_tags import get_upcoming_events, get_week_URL


class RenderUpcomingEventsTestCase(TestCase):
    """Tests for the ``render_upcoming_events`` tag."""
    longMessage = True

    def setUp(self):
        self.occurrence = mixer.blend(
            'calendarium.Occurrence',
            start=timezone.now() + timezone.timedelta(days=1),
            end=timezone.now() + timezone.timedelta(days=2),
            original_start=timezone.now() + timezone.timedelta(seconds=20),
            event__start=timezone.now() + timezone.timedelta(days=1),
            event__end=timezone.now() + timezone.timedelta(days=2),
            event__title='foo',
        )

    def test_render_tag(self):
        t = Template('{% load calendarium_tags %}{% render_upcoming_events %}')
        self.assertIn('foo', t.render(Context()))


class GetUpcomingEventsTestCase(TestCase):
    """Tests for the ``get_upcoming_events`` tag."""
    longMessage = True

    def setUp(self):
        self.occurrence = mixer.blend(
            'calendarium.Occurrence',
            start=timezone.now() + timezone.timedelta(days=1),
            end=timezone.now() + timezone.timedelta(days=2),
            original_start=timezone.now() + timezone.timedelta(seconds=20),
            event__start=timezone.now() + timezone.timedelta(days=1),
            event__end=timezone.now() + timezone.timedelta(days=2),
        )

    def test_tag(self):
        result = get_upcoming_events()
        self.assertEqual(len(result), 1)


class GetWeekURLTestCase(TestCase):
    """Tests for the ``get_week_URL`` tag."""
    longMessage = True

    def test_tag(self):
        result = get_week_URL(
            timezone.datetime.strptime('2016-02-07', '%Y-%m-%d'))
        self.assertEqual(result, u'/2016/week/5/')
