"""Tests for the models of the ``calendarium`` app."""
from django.test import TestCase
from django.utils.timezone import timedelta

from calendarium.models import (
    EventCategory,
    EventRelation,
    Occurrence,
    Rule,
)
from calendarium.models import Event
from calendarium.tests.factories import EventFactory, OccurrenceFactory
from calendarium.utils import now


class EventModelManagerTestCase(TestCase):
    """Tests for the ``EventModelManager`` custom manager."""
    longMessage = True

    def setUp(self):
        # event that only occurs once
        self.event = EventFactory(rule=None)
        # event that occurs for one week daily with one custom occurrence
        self.event_daily = EventFactory()
        self.occurrence = OccurrenceFactory(
            event=self.event, title='foo_occurrence')

    def test_get_occurrences(self):
        """Test for the ``get_occurrences`` manager method."""
        occurrences = Event.objects.get_occurrences(
            now(), now() + timedelta(days=7))
        self.assertEqual(len(occurrences), 8, msg=(
            '``get_occurrences`` should return the correct amount of'
            ' occurrences.'))

        occurrences = Event.objects.get_occurrences(now(), now())
        self.assertEqual(len(occurrences), 2, msg=(
            '``get_occurrences`` should return the correct amount of'
            ' occurrences for one day.'))


class EventTestCase(TestCase):
    """Tests for the ``Event`` model."""
    longMessage = True

    def setUp(self):
        self.not_found_event = EventFactory(
            set__start=-24, set__end=-24, set__creation_date=-24,
            rule=None)
        self.event = EventFactory()
        self.occurrence = OccurrenceFactory(
            event=self.event, title='foo_occurrence')
        self.single_time_event = EventFactory(rule=None)

    def test_create_occurrence(self):
        """Test for ``_create_occurrence`` method."""
        occurrence = self.event._create_occurrence(now())
        self.assertEqual(type(occurrence), Occurrence, msg=(
            'Method ``_create_occurrence`` did not output the right type.'))

    def test_get_occurrence_gen(self):
        """Test for the ``_get_occurrence_gen`` method"""
        occurrence_gen = self.event._get_occurrence_gen(
            now(), now() + timedelta(days=8))
        occ_list = [occ for occ in occurrence_gen]
        self.assertEqual(len(occ_list), 7, msg=(
            'The method ``_get_occurrence_list`` did not return the expected'
            ' amount of items.'))

        occurrence_gen = self.not_found_event._get_occurrence_gen(
            now(), now() + timedelta(days=8))
        occ_list = [occ for occ in occurrence_gen]
        self.assertEqual(len(occ_list), 0, msg=(
            'The method ``_get_occurrence_list`` did not return the expected'
            ' amount of items.'))

    def test_get_occurrences(self):
        occurrence_gen = self.event.get_occurrences(
            now(), now() + timedelta(days=7))
        occ_list = [occ for occ in occurrence_gen]
        self.assertEqual(len(occ_list), 7, msg=(
            'Method ``get_occurrences`` did not output the correct amount'
            ' of occurrences.'))
        occurrence_gen = self.event.get_occurrences(
            now(), now() + timedelta(days=7))
        self.assertEqual(occurrence_gen.next().title, 'foo_occurrence', msg=(
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
