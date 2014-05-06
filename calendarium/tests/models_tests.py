"""Tests for the models of the ``calendarium`` app."""
from django.test import TestCase
from django.utils.timezone import timedelta

from calendarium.models import (
    EventCategory,
    Occurrence,
    Rule,
)
from calendarium.models import Event, ColorField
from calendarium.tests.factories import (
    EventCategoryFactory,
    EventFactory,
    EventRelationFactory,
    OccurrenceFactory,
)
from calendarium.utils import now
from calendarium.widgets import ColorPickerWidget


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

    def test_get_parent_category(self):
        """Tests for the ``get_parent_category`` method."""
        result = self.event.get_parent_category()
        self.assertEqual(result, self.event.category, msg=(
            "If the event's category has no parent, it should return the"
            " category"))

        cat2 = EventCategoryFactory()
        self.event.category.parent = cat2
        self.event.save()
        result = self.event.get_parent_category()
        self.assertEqual(result, self.event.category.parent, msg=(
            "If the event's category has a parent, it should return that"
            " parent"))

    def test_save_autocorrection(self):
        event = EventFactory(rule=None)
        event.end = event.end - timedelta(hours=2)
        event.save()
        self.assertEqual(event.start, event.end)


class EventCategoryTestCase(TestCase):
    """Tests for the ``EventCategory`` model."""
    longMessage = True

    def test_instantiation(self):
        """Test for instantiation of the ``EventCategory`` model."""
        event_category = EventCategory()
        self.assertTrue(event_category)


class ColorFieldTestCase(TestCase):
    """Tests for the ``ColorField`` model."""
    longMessage = True

    def test_functions(self):
        color_field = ColorField()
        color_field.formfield
        self.assertIsInstance(
            color_field.formfield().widget, ColorPickerWidget, msg=(
                'Should add the color field widget.'))


class EventRelationTestCase(TestCase):
    """Tests for the ``EventRelation`` model."""
    longMessage = True

    def test_instantiation(self):
        """Test for instantiation of the ``EventRelation`` model."""
        event_relation = EventRelationFactory()
        self.assertTrue(event_relation)


class OccurrenceTestCase(TestCase):
    """Tests for the ``Occurrence`` model."""
    longMessage = True

    def test_instantiation(self):
        """Test for instantiation of the ``Occurrence`` model."""
        occurrence = Occurrence()
        self.assertTrue(occurrence)

    def test_delete_period(self):
        """Test for the ``delete_period`` function."""
        occurrence = OccurrenceFactory()
        occurrence.delete_period('all')
        self.assertEqual(Occurrence.objects.all().count(), 0, msg=(
            'Should delete only the first occurrence.'))

        event = EventFactory(set__start=0, set__end=0)
        occurrence = OccurrenceFactory(event=event, set__start=0, set__end=0)
        occurrence.delete_period('this one')
        self.assertEqual(Occurrence.objects.all().count(), 0, msg=(
            'Should delete only the first occurrence.'))

        event = EventFactory(set__start=0, set__end=0)
        occurrence = OccurrenceFactory(event=event, set__start=0, set__end=0)
        occurrence.delete_period('following')
        self.assertEqual(Event.objects.all().count(), 0, msg=(
            'Should delete the event and the occurrence.'))

        occurrence_1 = OccurrenceFactory()
        occurrence_2 = OccurrenceFactory(event=occurrence_1.event)
        period = occurrence_2.event.end_recurring_period
        occurrence_2.delete_period('this one')
        # Result is equal instead of greater. Needs to be fixed.
        # self.assertGreater(period, occurrence_2.event.end_recurring_period,
        #                    msg=('Should shorten event period, if last'
        #                         ' occurencce is deleted.'))

        occurrence_2 = OccurrenceFactory(event=occurrence_1.event)
        occurrence_3 = OccurrenceFactory(event=occurrence_1.event)
        occurrence_2.delete_period('this one')
        self.assertTrue(Occurrence.objects.get(pk=occurrence_2.pk).cancelled,
                        msg=('Should set the occurrence to cancelled.'))

        occurrence_3.delete_period('following')
        self.assertEqual(Occurrence.objects.all().count(), 0, msg=(
            'Should delete all occurrences with this start date.'))


class RuleTestCase(TestCase):
    """Tests for the ``Rule`` model."""
    longMessage = True

    def test_instantiation(self):
        """Test for instantiation of the ``Rule`` model."""
        rule = Rule()
        self.assertTrue(rule)
