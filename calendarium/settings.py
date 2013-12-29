"""Default settings for the calendarium app."""
from django.conf import settings


SHIFT_WEEKSTART = getattr(settings, 'CALENDARIUM_SHIFT_WEEKSTART', 0)
