"""Settings that need to be set in order to run the tests."""
import os

DEBUG = True
USE_TZ = True
TIME_ZONE = 'Asia/Singapore'

AUTH_USER_MODEL = 'auth.User'

SITE_ID = 1

SECRET_KEY = 'Foobar'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = 'calendarium.tests.urls'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(__file__, '../../static/')

STATICFILES_DIRS = (
    os.path.join(__file__, 'test_static'),
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), '../templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)

COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__), 'coverage')

COVERAGE_MODULE_EXCLUDES = [
    'tests$', 'settings$', 'urls$', 'locale$',
    'migrations', 'fixtures', 'admin$', 'django_extensions',
]

EXTERNAL_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django_nose',
    'filer',
]

INTERNAL_APPS = [
    'calendarium',
]

TEST_APPS = [
    'calendarium.tests.test_app',
]

INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS + TEST_APPS

COVERAGE_MODULE_EXCLUDES += EXTERNAL_APPS
