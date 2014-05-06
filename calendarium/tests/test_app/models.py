"""Models for the ``test_app`` test app."""
import factory

from django.db import models


class DummyModel(models.Model):
    """
    This is a dummy model for testing purposes.

    :content: Just a dummy field.

    """
    content = models.CharField(
        max_length=32,
    )


class DummyModelFactory(factory.DjangoModelFactory):
    """Factory for the ``DummyModel`` model."""
    FACTORY_FOR = DummyModel

    content = factory.Sequence(lambda n: 'content{0}'.format(n))
