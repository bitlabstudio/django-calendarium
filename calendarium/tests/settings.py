"""
These settings are used by the ``manage.py`` command.
With normal tests we want to use the fastest possible way which is an
in-memory sqlite database but if you want to create South migrations you
need a persistant database.
Unfortunately there seems to be an issue with either South or syncdb so that
defining two routers ("default" and "south") does not work.
"""
from distutils.version import StrictVersion

import django

from .test_settings import *  # NOQA


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
    }
}

django_version = django.get_version()
if StrictVersion(django_version) < StrictVersion('1.7'):
    INSTALLED_APPS.append('south', )
