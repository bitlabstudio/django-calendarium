"""Factories for the models of the ``calendarium`` app."""
import factory

from django_libs.tests.factories import UserFactory
from django.utils import timezone

from calendarium.models import (
    Event,
    EventCategory,
    EventRelation,
    Occurrence,
    Rule,
)
from calendarium.tests.test_app.models import DummyModelFactory


class EventCategoryFactory(factory.Factory):
    """Factory for the ``EventCategory`` model."""
    FACTORY_FOR = EventCategory

    name = factory.Sequence(lambda n: 'category{0}'.format(n))
    color = factory.Sequence(lambda n: 'col{0}'.format(n))


class EventFactoryMixin(factory.Factory):
    """Mixin for the event models."""
    FACTORY_FOR = None

    start = timezone.now()
    end = timezone.now()
    title = factory.Sequence(lambda n: 'title{0}'.format(n))
    description = factory.Sequence(lambda n: 'description{0}'.format(n))
    created_by = factory.SubFactory(UserFactory)
    creation_date = timezone.now()


class RuleFactory(factory.Factory):
    """Factory for the ``Rule`` model."""
    FACTORY_FOR = Rule

    name = factory.Sequence(lambda n: 'rule{0}'.format(n))
    description = factory.Sequence(lambda n: 'description{0}'.format(n))
    frequency = factory.Sequence(lambda n: 'frequency{0}'.format(n))
    params = 'JSON STRING'


class EventFactory(EventFactoryMixin):
    """Factory for the ``Event`` model."""
    FACTORY_FOR = Event

    category = factory.SubFactory(EventCategoryFactory)
    rule = factory.SubFactory(RuleFactory)
    end_recurring_period = timezone.now()

    @factory.post_generation(extract_prefix='set')
    def time_offset(self, create, extracted, **kwargs):
        """
        On initialization of the Factory one can pass following argument:

            'set__fieldname=value'

        where fieldname is the name of the field to set (e.g. start) and value
        is the time offset in days to set.

        To set start 4 days into the past you would pass the following:

            'set__start=-4'

        """
        self.creation_date = timezone.now() - timezone.timedelta(
            days=kwargs.get('creation_date') or 0)
        self.start = timezone.now() - timezone.timedelta(
            days=kwargs.get('start') or 0)
        self.end = timezone.now() - timezone.timedelta(
            days=kwargs.get('end') or 0)
        self.end_recurring_period = timezone.now() - timezone.timedelta(
            days=kwargs.get('end_recurring_period') or 0)
        if create:
            self.save()


class EventRelation(factory.Factory):
    """Factory for the ``EventRelation`` model."""
    FACTORY_FOR = EventRelation

    event = factory.SubFactory(EventFactory)
    content_object = factory.SubFactory(DummyModelFactory)
    relation_type = factory.Sequence(lambda n: 'relation_type{0}'.format(n))


class OccurrenceFactory(EventFactoryMixin):
    """Factory for the ``Occurrence`` model."""
    FACTORY_FOR = Occurrence

    event = factory.SubFactory(EventFactory)
    original_start = timezone.now()
    original_end = timezone.now()

    @factory.post_generation(extract_prefix='set')
    def time_offset(self, create, extracted, **kwargs):
        """
        On initialization of the Factory one can pass following argument:

            'set__fieldname=value'

        where fieldname is the name of the field to set (e.g. start) and value
        is the time offset in days to set.

        To set start 4 days into the past you would pass the following:

            'set__start=-4'

        """
        self.creation_date = timezone.now() - timezone.timedelta(
            days=kwargs.get('creation_date') or 0)
        self.start = timezone.now() - timezone.timedelta(
            days=kwargs.get('start') or 0)
        self.end = timezone.now() - timezone.timedelta(
            days=kwargs.get('end') or 0)
        self.original_start = timezone.now() - timezone.timedelta(
            days=kwargs.get('original_start') or 0)
        self.original_end = timezone.now() - timezone.timedelta(
            days=kwargs.get('original_end') or 0)
        if create:
            self.save()
