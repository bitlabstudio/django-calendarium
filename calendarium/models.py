"""
Models for the ``calendarium`` app.

The code of these models is highly influenced by or taken from the models of
django-schedule:

https://github.com/thauber/django-schedule/tree/master/schedule/models

"""
import json
from dateutil import rrule

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from calendarium.constants import FREQUENCY_CHOICES
from calendarium.utils import OccurrenceReplacer


class EventModelManager(models.Manager):
    """Custom manager for the ``Event`` model class."""
    def get_occurrences(self, start, end):
        """Returns a list of events and occurrences for the given period."""
        # get events of which the end_recurring_period is after the start
        # of this period and the start is before the end of this period
        # if they do not have a end_recurring_period, their end needs to end
        # before the period starts

        # get all occurrences for those events that don't already have a
        # persistent match and that lie in this period.
            # This should be done by calling the get_occurrences() method of
            # each event previously fetched.

            # the get_occurences method should itself replace all persistent
            # occurrences for the calling event, compute events that are in the
            # given period and so only return appendable data

        # sort and return


class EventModelMixin(models.Model):
    """
    Base event mixin class to prevent recurrence in the ``Event`` and
    ``Occurrence`` model class.

    """
    start = models.DateTimeField(
        verbose_name=_('Start date'),
    )

    end = models.DateTimeField(
        verbose_name=_('End date'),
    )

    title = models.CharField(
        max_length=256,
        verbose_name=_('Title'),
    )

    description = models.TextField(
        max_length=2048,
        verbose_name=_('Description'),
    )

    creation_date = models.DateTimeField(
        verbose_name=_('Creation date'),
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class Event(EventModelMixin):
    """
    Hold the information about an event in the calendar.

    inherited from ``EventModelMixin``:
        :start: The start date of the event.
        :end: The end date of the event.
        :title: The title of the event.
        :description: The description of the event.
        :creation_date: When this event was created.
    own:
        :created_by: FK to the ``User``, who created this event.
        :category: FK to the ``EventCategory`` this event belongs to.
        :rule: FK to the definition of the recurrence of an event.
        :end_recurring_period: The possible end of the recurring definition.

    """

    created_by = models.ForeignKey(
        'auth.User',
        verbose_name=_('Created by'),
        related_name='events',
    )

    category = models.ForeignKey(
        'EventCategory',
        verbose_name=_('Category'),
        related_name='events',
    )

    rule = models.ForeignKey(
        'Rule',
        verbose_name=_('Rule'),
        blank=True, null=True,
    )

    end_recurring_period = models.DateTimeField(
        verbose_name=_('End of recurring'),
    )

    def _create_occurrence(self, occ_start, occ_end=None):
        """Creates an Occurrence instance."""
        # if the length is not altered, it is okay to only pass occ_start
        if not occ_end:
            occ_end = occ_start + (self.end - self.start)
        return Occurrence(
            event=self, start=occ_start, end=occ_end,
            # TODO not sure why original start and end also are occ_start/_end
            original_start=occ_start, original_end=occ_end,
            title=self.title, description=self.description,
            creation_date=self.creation_date, created_by=self.created_by)

    def _get_occurrence_list(self, start, end):
        """Computes all occurrences for this event from start to end."""
        # get length of the event
        length = self.end - self.start

        if self.rule:
            # if the end of the recurring period is before the end arg passed
            # the end of the recurring period should be the new end
            if self.end_recurring_period and self.end_recurring_period < end:
                end = self.end_recurring_period
            # get all the starts of the occs that end in the poriod
            rr = self.get_rrule_object()
            occ_start_list = rr.between(start - length, end, inc=True)
            # create the occurrences of the period
            occurrences = []
            for occ_start in occ_start_list:
                occ_end = occ_start + length
                occurrences.append(self._create_occurrence(occ_start, occ_end))
            return occurrences

    def get_occurrences(self, start, end):
        """Returns all occurrences from start to end."""
        # get persistent occurrences
        # TODO already filter instead of adding them in the end?
        persistent_occurrences = self.occurrences.all()

        # setup occ_replacer with p_occs
        occ_replacer = OccurrenceReplacer(persistent_occurrences)

        # compute own occurrences according to rule that overlap with the
        # period
        occurrences = self._get_occurrence_list(start, end)
        # merge computed with persistent using the occ_replacer
        final_occurrences = []
        for occ in occurrences:
            # check if there is a matching persistent occ and get it if true
            if occ_replacer.has_occurrence(occ):
                p_occ = occ_replacer.get_occurrence(occ)

                # if the persistent occ falls into the period, replace it
                if p_occ.start < end and p_occ.end >= start:
                    final_occurrences.append(p_occ)
            else:
                # if there is no persistent match, use the original occ
                final_occurrences.append(occ)
        # then add persisted occurrences which originated outside of this
        # period but now fall within it
        final_occurrences += occ_replacer.get_additional_occurrences(
            start, end)
        return final_occurrences

    def get_rrule_object(self):
        """Returns the rrule object for this ``Event``."""
        if self.rule:
            params = self.rule.get_params()
            frequency = 'rrule.{0}'.format(self.rule.frequency)
            return rrule.rrule(eval(frequency), dtstart=self.start, **params)


class EventCategory(models.Model):
    """The category of an event."""
    name = models.CharField(
        max_length=256,
        verbose_name=_('Name'),
    )

    color = models.CharField(
        max_length=6,
        verbose_name=_('Color'),
    )


class EventRelation(models.Model):
    """
    This class allows to relat additional or external data to an event.

    :event: A FK to the ``Event`` this additional data is related to.
    :content_type: A FK to ContentType of the generic object.
    :object_id: The id of the generic object.
    :content_object: The generic foreign key to the generic object.
    :relation_type: A string representing the type of the relation.

    """

    event = models.ForeignKey(
        'Event',
        verbose_name=_("Event"),
    )

    content_type = models.ForeignKey(
        ContentType,
    )

    object_id = models.IntegerField()

    content_object = generic.GenericForeignKey(
        'content_type',
        'object_id',
    )

    relation_type = models.CharField(
        verbose_name=_('Relation type'),
        max_length=32,
        blank=True, null=True,
    )


class Occurrence(EventModelMixin):
    """
    Needed for re-scheduling an occurrence of an ``Event``.

    inherited from ``EventModelMixin``:
        :start: The start date of the event.
        :end: The end date of the event.
        :title: The title of the event.
        :description: The description of the event.
        :creation_date: When this event was created.
    own:
        :created_by: FK to the ``User``, who created this event.
        :event: FK to the ``Event`` this ``Occurrence`` belongs to.
        :original_start: The original start of the related ``Event``.
        :original_end: The original end of the related ``Event``.

    """
    created_by = models.ForeignKey(
        'auth.User',
        verbose_name=_('Created by'),
        related_name='occurrences',
    )

    event = models.ForeignKey(
        'Event',
        verbose_name=_('Event'),
        related_name='occurrences',
    )

    original_start = models.DateTimeField(
        verbose_name=_('Original start'),
    )

    original_end = models.DateTimeField(
        verbose_name=_('Original end'),
    )

    cancelled = models.BooleanField(
        verbose_name=_('Cancelled'),
    )


class Rule(models.Model):
    """
    This defines the rule by which an event will recur.

    :name: Name of this rule.
    :description: Description of this rule.
    :frequency: A string representing the frequency of the recurrence.
    :params: JSON string to hold the exact rule parameters to define the
        pattern of the recurrence

    """
    name = models.CharField(
        verbose_name=_("name"),
        max_length=32,
    )

    description = models.TextField(
        _("description"),
    )

    frequency = models.CharField(
        verbose_name=_("frequency"),
        choices=FREQUENCY_CHOICES,
        max_length=10,
    )

    params = models.TextField(
        verbose_name=_("params"),
        blank=True, null=True,
    )

    def get_params(self):
        return json.loads(self.params)
