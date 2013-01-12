"""Tests for the models of the ``calendarium`` app."""
from django.test import TestCase
from django.utils.timezone import timedelta

from calendarium.models import (
    EventCategory,
    EventRelation,
    Occurrence,
    Rule,
)
from calendarium.tests.factories import EventFactory, OccurrenceFactory
from calendarium.utils import now


class EventTestCase(TestCase):
    """Tests for the ``Event`` model."""
    longMessage = True

    def setUp(self):
        self.event = EventFactory()
        self.occurrence = OccurrenceFactory(
            event=self.event, title='foo_occurrence')

    def test_create_occurrence(self):
        """Test for ``_create_occurrence`` method."""
        occurrence = self.event._create_occurrence(now())
        self.assertEqual(type(occurrence), Occurrence, msg=(
            'Method ``_create_occurrence`` did not output the right type.'))

    def test_get_occurrence_list(self):
        """Test for the ``_get_occurrence_list`` method"""
        occurrence_list = self.event._get_occurrence_list(
            now(), now() + timedelta(days=8))
        self.assertEqual(len(occurrence_list), 7, msg=(
            'The method ``_get_occurrence_list`` did not return the expected'
            ' amount of items.'))

    def test_get_occurrences(self):
        occurrences = self.event.get_occurrences(
            now(), now() + timedelta(days=7))
        self.assertEqual(len(occurrences), 7, msg=(
            'Method ``get_occurrences`` did not output the correct amount'
            ' of occurrences.'))
        self.assertEqual(occurrences[0].title, 'foo_occurrence', msg=(
            'The persistent occurrence should have been first in the list.'))


class EventCategoryTestCase(TestCase):
    """Tests for the ``EventCategory`` model."""
    longMessage = True

    def test_instantiation(self):
        """Test for instantiation of the ``EventCategory`` model."""
        event_category = EventCategory()
        self.assertTrue(event_category)


class EventRelationTestCase(TestCase):
    """Tests for the ``EventRelation`` model."""
    longMessage = True

    def test_instantiation(self):
        """Test for instantiation of the ``EventRelation`` model."""
        event_relation = EventRelation()
        self.assertTrue(event_relation)


class OccurrenceTestCase(TestCase):
    """Tests for the ``Occurrence`` model."""
    longMessage = True

    def test_instantiation(self):
        """Test for instantiation of the ``Occurrence`` model."""
        occurrence = Occurrence()
        self.assertTrue(occurrence)


class RuleTestCase(TestCase):
    """Tests for the ``Rule`` model."""
    longMessage = True

    def test_instantiation(self):
        """Test for instantiation of the ``Rule`` model."""
        rule = Rule()
        self.assertTrue(rule)
