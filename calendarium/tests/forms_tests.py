"""Tests for the forms of the ``calendarium`` app."""
import json

from django.forms.models import model_to_dict
from django.test import TestCase
from django.utils.timezone import timedelta

from mixer.backend.django import mixer

from ..constants import FREQUENCIES, OCCURRENCE_DECISIONS
from ..forms import OccurrenceForm
from ..models import Event, Occurrence
from ..utils import now


class OccurrenceFormTestCase(TestCase):
    """Test for the ``OccurrenceForm`` form class."""
    longMessage = True

    def setUp(self):
        # single, not recurring event
        self.event = mixer.blend('calendarium.Event', rule=None,
                                 end_recurring_period=None)
        self.event_occurrence = next(self.event.get_occurrences(
            self.event.start))

        # recurring event weekly on mondays over 6 weeks
        self.rule = mixer.blend(
            'calendarium.Rule',
            name='weekly', frequency=FREQUENCIES['WEEKLY'],
            params=json.dumps({'byweekday': 0}))
        self.rec_event = mixer.blend(
            'calendarium.Event',
            rule=self.rule, start=now(),
            end_recurring_period=now() + timedelta(days=41),
        )
        self.rec_occurrence_list = [
            occ for occ in self.rec_event.get_occurrences(
                self.rec_event.start, self.rec_event.end_recurring_period)]
        self.rec_occurrence = self.rec_occurrence_list[1]

    def test_form(self):
        """Test if ``OccurrenceForm`` is valid and saves correctly."""
        # Test for not recurring event
        data = model_to_dict(self.event_occurrence)
        initial = data.copy()
        data.update({
            'decision': OCCURRENCE_DECISIONS['all'],
            'title': 'changed'})
        form = OccurrenceForm(data=data, initial=initial)
        self.assertTrue(form.is_valid(), msg=(
            'The OccurrenceForm should be valid'))
        form.save()
        event = Event.objects.get(pk=self.event.pk)
        self.assertEqual(event.title, 'changed', msg=(
            'When save is called, the event\'s title should be "changed".'))

        # Test for recurring event

        # Case 1: Altering occurrence 3 to be on a tuesday.
        data = model_to_dict(self.rec_occurrence)
        initial = data.copy()
        data.update({
            'decision': OCCURRENCE_DECISIONS['this one'],
            'title': 'different'})
        form = OccurrenceForm(data=data, initial=initial)
        self.assertTrue(form.is_valid(), msg=(
            'The OccurrenceForm should be valid'))
        form.save()
        self.assertEqual(Occurrence.objects.all().count(), 1, msg=(
            'After one occurrence has changed, there should be one persistent'
            ' occurrence.'))
        occ = Occurrence.objects.get()
        self.assertEqual(occ.title, 'different', msg=(
            'When save is called, the occurrence\'s title should be'
            ' "different".'))

        # Case 2: Altering the description of "all" on the first occurrence
        # should also change 3rd one
        occ_to_use = self.rec_occurrence_list[0]
        data = model_to_dict(occ_to_use)
        initial = data.copy()
        new_start = occ_to_use.start + timedelta(hours=1)
        data.update({
            'decision': OCCURRENCE_DECISIONS['all'],
            'description': 'has changed',
            'start': new_start})
        form = OccurrenceForm(data=data, initial=initial)
        self.assertTrue(form.is_valid(), msg=(
            'The OccurrenceForm should be valid'))
        form.save()
        self.assertEqual(Occurrence.objects.all().count(), 1, msg=(
            'After one occurrence has changed, there should be one persistent'
            ' occurrence.'))
        occ = Occurrence.objects.get()
        self.assertEqual(occ.title, 'different', msg=(
            'When save is called, the occurrence\'s title should still be'
            ' "different".'))
        self.assertEqual(occ.description, 'has changed', msg=(
            'When save is called, the occurrence\'s description should be'
            ' "has changed".'))
        self.assertEqual(
            occ.start, self.rec_occurrence.start + timedelta(hours=1), msg=(
                'When save is called, the occurrence\'s start time should be'
                ' set forward one hour.'))

        # Case 3: Altering everything from occurrence 4 to 6 to one day later
        occ_to_use = self.rec_occurrence_list[4]
        data = model_to_dict(occ_to_use)
        initial = data.copy()
        new_start = occ_to_use.start - timedelta(days=1)
        data.update({
            'decision': OCCURRENCE_DECISIONS['following'],
            'start': new_start})
        form = OccurrenceForm(data=data, initial=initial)
        self.assertTrue(form.is_valid(), msg=(
            'The OccurrenceForm should be valid'))
        form.save()
        self.assertEqual(Event.objects.all().count(), 3, msg=(
            'After changing occurrence 4-6, a new event should have been'
            ' created.'))
        event1 = Event.objects.get(pk=self.rec_event.pk)
        event2 = Event.objects.exclude(
            pk__in=[self.rec_event.pk, self.event.pk]).get()
        self.assertEqual(
            event1.end_recurring_period,
            event2.start - timedelta(days=1), msg=(
                'The end recurring period of the old event should be the same'
                ' as the start of the new event minus one day.'))
        self.assertEqual(
            event2.end_recurring_period, self.rec_event.end_recurring_period,
            msg=(
                'The end recurring period of the new event should be the'
                ' old end recurring period of the old event.'))
        # -> should yield 2 events, one newly created one altered
