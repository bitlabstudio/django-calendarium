"""Models for the ``test_app`` test app."""
from django.db import models


class DummyModel(models.Model):
    """
    This is a dummy model for testing purposes.

    :content: Just a dummy field.

    """
    content = models.CharField(
        max_length=32,
    )
