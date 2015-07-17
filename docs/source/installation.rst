Installation
============

If you want to install the latest stable release from PyPi::

    $ pip install django-calendarium

If you feel adventurous and want to install the latest commit from GitHub::

    $ pip install -e git+git://github.com/bitmazk/django-calendarium.git#egg=calendarium

Add ``calendarium`` (and the ``filer`` dependencies) to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'filer',
        'mptt',
        'easy_thumbnails',
        'calendarium',
    )

Add ``django.core.context_processors.request`` to your ``TEMPLATE_CONTEXT_PROCESSORS``::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...,
        'django.core.context_processors.request',
    )

Add the urls to your main ``urls.py``::

    urlpatterns = patterns('',
        ...
        url(r'^calendar/', include('calendarium.urls')),
    )

If you are using a Django version below 1.7, add the following setting:

SOUTH_MIGRATION_MODULES = {
    'calendarium': 'calendarium.south_migrations',
}

Run the migrations::

    ./manage.py migrate
