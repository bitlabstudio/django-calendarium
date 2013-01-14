"""Factories for the models of the ``calendarium`` app."""
import factory

from django_libs.tests.factories import UserFactory
from django.utils.timezone import timedelta

from calendarium.models import (
    Event,
    EventCategory,
    EventRelation,
    Occurrence,
    Rule,
)
from calendarium.tests.test_app.models import DummyModelFactory
from calendarium.utils import now


class EventCategoryFactory(factory.Factory):
    """Factory for the ``EventCategory`` model."""
    FACTORY_FOR = EventCategory

    name = factory.Sequence(lambda n: 'category{0}'.format(n))
    color = factory.Sequence(lambda n: 'col{0}'.format(n))


class EventFactoryMixin(factory.Factory):
    """Mixin for the event models."""
    FACTORY_FOR = None

    start = now()
    end = now() + timedelta(hours=1)
    title = factory.Sequence(lambda n: 'title{0}'.format(n))
    description = factory.Sequence(lambda n: 'description{0}'.format(n))
    created_by = factory.SubFactory(UserFactory)
    creation_date = now()


class RuleFactory(factory.Factory):
    """Factory for the ``Rule`` model."""
    FACTORY_FOR = Rule

    name = factory.Sequence(lambda n: 'rule{0}'.format(n))
    description = factory.Sequence(lambda n: 'description{0}'.format(n))
    # standard is set to DAILY and one week long
    frequency = 'DAILY'
    params = '{"count": 7}'


class EventFactory(EventFactoryMixin):
    """
    Factory for the ``Event`` model.

    If you set rule=None on creation, you get an event that occurs only once.
    Otherwise it defaults to an event with a DAILY rule over one week.

    """
    FACTORY_FOR = Event

    category = factory.SubFactory(EventCategoryFactory)
    rule = factory.SubFactory(RuleFactory)
    end_recurring_period = now()

    @factory.post_generation(extract_prefix='set')
    def time_offset(self, create, extracted, **kwargs):
        """
        On initialization of the Factory one can pass following argument:

            'set__fieldname=value'

        where fieldname is the name of the field to set (e.g. start) and value
        is the time offset in hours to set.

        To set start 4 hours into the past you would pass the following:

            'set__start=-4'

        """
        self.creation_date = now() - timedelta(
            hours=kwargs.get('creation_date') or 0)
        self.start = now() + timedelta(hours=kwargs.get('start') or 0)
        if kwargs.get('end') is not None:
            self.end = now() + timedelta(hours=kwargs.get('end'))
        else:
            self.end = now() + timedelta(hours=1)
        # note that this defaults to seven, because the default rule is daily
        # for one week, so 7 days
        if self.rule:
            self.end_recurring_period = now() + timedelta(
                hours=kwargs.get('end_recurring_period') or 0, days=7)
        else:
            self.end_recurring_period = None
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
    original_start = now()
    original_end = now() + timedelta(hours=1)

    @factory.post_generation(extract_prefix='set')
    def time_offset(self, create, extracted, **kwargs):
        """
        On initialization of the Factory one can pass following argument:

            'set__fieldname=value'

        where fieldname is the name of the field to set (e.g. start) and value
        is the time offset in hours to set.

        To set start 4 hours into the past you would pass the following:

            'set__start=-4'

        """
        self.creation_date = now() + timedelta(
            hours=kwargs.get('creation_date') or 0)
        self.start = now() + timedelta(
            hours=kwargs.get('start') or 0)
        self.end = now() + timedelta(
            hours=kwargs.get('end') or 0)
        self.original_start = now() + timedelta(
            hours=kwargs.get('original_start') or 0)
        if kwargs.get('original_end') is not None:
            self.original_end = now() + timedelta(hours=kwargs.get(
                'original_end'))
        else:
            self.original_end = now() + timedelta(hours=1)
        if create:
            self.save()
