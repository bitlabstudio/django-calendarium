Installation
============

If you want to install the latest stable release from PyPi::

    $ pip install django-calendarium

If you feel adventurous and want to install the latest commit from GitHub::

    $ pip install -e git+git://github.com/bitmazk/django-calendarium.git#egg=calendarium

Add ``calendarium`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'calendarium',
    )

Add the urls to your main ``urls.py``::

    urlpatterns = patterns('',
        ...
        url(r'^calendar/', include('calendarium.urls')),
    )

Run the South migrations::

    ./manage.py migrate calendarium
