"""Models for the ``calendarium`` app."""
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from calendarium.constants import FREQUENCY_CHOICES


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
    )

    end_recurring_period = models.DateTimeField(
        verbose_name=_('End of recurring'),
    )


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
    content_type: A FK to ContentType of the generic object.
    object_id: The id of the generic object.
    content_object: The generic foreign key to the generic object.
    relation_type: A string representing the type of the relation.

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
