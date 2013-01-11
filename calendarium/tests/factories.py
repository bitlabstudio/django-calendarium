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


class EventFactoryMixin(object):
    """Mixin for the event models."""
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


class EventFactory(EventFactoryMixin, factory.Factory):
    """Factory for the ``Event`` model."""
    FACTORY_FOR = Event

    category = factory.SubFactory(EventCategoryFactory)
    rule = factory.SubFactory(RuleFactory)
    end_recurring_period = timezone.now()


class EventRelation(factory.Factory):
    """Factory for the ``EventRelation`` model."""
    FACTORY_FOR = EventRelation

    event = factory.SubFactory(EventFactory)
    content_object = factory.SubFactory(DummyModelFactory)
    relation_type = factory.Sequence(lambda n: 'relation_type{0}'.format(n))


class OccurrenceFactory(EventFactoryMixin, factory.Factory):
    """Factory for the ``Occurrence`` model."""
    FACTORY_FOR = Occurrence

    event = factory.SubFactory(EventFactory)
    original_start = timezone.now()
    original_end = timezone.now()
