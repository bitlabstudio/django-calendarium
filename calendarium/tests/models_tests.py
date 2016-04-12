"""Tests for the models of the ``calendarium`` app."""
from django.test import TestCase
from django.utils.timezone import timedelta

from mixer.backend.django import mixer

from ..models import Event, EventCategory, Occurrence, Rule
from ..utils import now


class EventModelManagerTestCase(TestCase):
    """Tests for the ``EventModelManager`` custom manager."""
    longMessage = True

    def setUp(self):
        # event that only occurs once
        self.event = mixer.blend('calendarium.Event', rule=None, start=now(),
                                 end=now() + timedelta(hours=1))
        # event that occurs for one week daily with one custom occurrence
        self.event_daily = mixer.blend('calendarium.Event')
        self.occurrence = mixer.blend(
            'calendarium.Occurrence', event=self.event, original_start=now(),
            original_end=now() + timedelta(days=1), title='foo_occurrence')

    def test_get_occurrences(self):
        """Test for the ``get_occurrences`` manager method."""
        occurrences = Event.objects.get_occurrences(
            now(), now() + timedelta(days=7))
        self.assertEqual(len(occurrences), 1, msg=(
            '``get_occurrences`` should return the correct amount of'
            ' occurrences.'))

        occurrences = Event.objects.get_occurrences(now(), now())
        self.assertEqual(len(occurrences), 1, msg=(
            '``get_occurrences`` should return the correct amount of'
            ' occurrences for one day.'))


class EventTestCase(TestCase):
    """Tests for the ``Event`` model."""
    longMessage = True

    def setUp(self):
        self.not_found_event = mixer.blend(
            'calendarium.Event', start=now() - timedelta(hours=24),
            end=now() - timedelta(hours=24),
            creation_date=now() - timedelta(hours=24), rule=None)
        self.event = mixer.blend(
            'calendarium.Event', start=now(), end=now(),
            rule__frequency='DAILY', creation_date=now(),
            category=mixer.blend('calendarium.EventCategory'))
        self.occurrence = mixer.blend(
            'calendarium.Occurrence', original_start=now(),
            original_end=now() + timedelta(days=1), event=self.event,
            title='foo_occurrence')
        self.single_time_event = mixer.blend('calendarium.Event', rule=None)

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
        self.assertEqual(len(occ_list), 8, msg=(
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
        self.assertEqual(len(occ_list), 6, msg=(
            'Method ``get_occurrences`` did not output the correct amount'
            ' of occurrences.'))

    def test_get_parent_category(self):
        """Tests for the ``get_parent_category`` method."""
        result = self.event.get_parent_category()
        self.assertEqual(result, self.event.category, msg=(
            "If the event's category has no parent, it should return the"
            " category"))

        cat2 = mixer.blend('calendarium.EventCategory')
        self.event.category.parent = cat2
        self.event.save()
        result = self.event.get_parent_category()
        self.assertEqual(result, self.event.category.parent, msg=(
            "If the event's category has a parent, it should return that"
            " parent"))

    def test_save_autocorrection(self):
        event = mixer.blend(
            'calendarium.Event', rule=None, start=now(),
            end=now() + timedelta(hours=1), creation_date=now())
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


class EventRelationTestCase(TestCase):
    """Tests for the ``EventRelation`` model."""
    longMessage = True

    def test_instantiation(self):
        """Test for instantiation of the ``EventRelation`` model."""
        event_relation = mixer.blend('calendarium.EventRelation')
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
        occurrence = mixer.blend('calendarium.Occurrence')
        occurrence.delete_period('all')
        self.assertEqual(Occurrence.objects.all().count(), 0, msg=(
            'Should delete only the first occurrence.'))

        event = mixer.blend(
            'calendarium.Event', start=now() - timedelta(hours=0),
            end=now() - timedelta(hours=0))
        occurrence = mixer.blend(
            'calendarium.Occurrence', event=event,
            start=now() - timedelta(hours=0), end=now() - timedelta(hours=0))
        occurrence.delete_period('this one')
        self.assertEqual(Occurrence.objects.all().count(), 0, msg=(
            'Should delete only the first occurrence.'))

        event = mixer.blend(
            'calendarium.Event', start=now() - timedelta(hours=0),
            end=now() - timedelta(hours=0))
        event.save()
        occurrence = mixer.blend(
            'calendarium.Occurrence', event=event,
            start=now() - timedelta(hours=0), end=now() - timedelta(hours=0))
        occurrence.delete_period('following')
        self.assertEqual(Event.objects.all().count(), 0, msg=(
            'Should delete the event and the occurrence.'))

        occurrence_1 = mixer.blend(
            'calendarium.Occurrence', start=now(),
            end=now() + timedelta(days=1),
            original_start=now() + timedelta(hours=1))
        occurrence_2 = mixer.blend(
            'calendarium.Occurrence', start=now(),
            end=now() + timedelta(days=1),
            original_start=now() + timedelta(hours=1))
        occurrence_2.event = occurrence_1.event
        occurrence_2.save()
        occurrence_2.delete_period('this one')
        # Result is equal instead of greater. Needs to be fixed.
        # self.assertGreater(period, occurrence_2.event.end_recurring_period,
        #                    msg=('Should shorten event period, if last'
        #                         ' occurencce is deleted.'))

        occurrence_3 = mixer.blend(
            'calendarium.Occurrence', start=now(),
            end=now() + timedelta(days=1),
            original_start=now() + timedelta(hours=1))
        occurrence_3.event = occurrence_1.event
        occurrence_3.save()
        occurrence_4 = mixer.blend(
            'calendarium.Occurrence', start=now(),
            end=now() + timedelta(days=1),
            original_start=now() + timedelta(hours=1))
        occurrence_4.event = occurrence_1.event
        occurrence_4.save()
        occurrence_3.delete_period('this one')
        occurrence_1.delete_period('following')
        self.assertEqual(Occurrence.objects.all().count(), 0, msg=(
            'Should delete all occurrences with this start date.'))


class RuleTestCase(TestCase):
    """Tests for the ``Rule`` model."""
    longMessage = True

    def test_instantiation(self):
        """Test for instantiation of the ``Rule`` model."""
        rule = Rule()
        self.assertTrue(rule)
