"""Tests for the template tags of the ``calendarium`` app."""
from django.template import Context, Template
from django.test import TestCase
from django.utils import timezone

from .factories import OccurrenceFactory


class RenderUpcomingEventsTestCase(TestCase):
    """Tests for the ``render_upcoming_events`` tag."""
    longMessage = True

    def setUp(self):
        self.occurrence = OccurrenceFactory(
            original_start=timezone.now() + timezone.timedelta(seconds=20))

    def test_render_tag(self):
        t = Template('{% load calendarium_tags %}{% render_upcoming_events %}')
        self.assertIn('{0}'.format(self.occurrence.title), t.render(Context()))
