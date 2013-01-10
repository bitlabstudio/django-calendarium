Django Calendarium
==================

EARLY ALPHA! DO NOT USE THIS!

A Django application for managing and displaying a calendar and it's events
in your templates.

It will be heavily influenced by the awesome
`django-schedule <https://github.com/thauber/django-schedule>`_

Since that project is unfortunately no longer maintained, we will try to revive
it's ideas with TDD, class based views and AJAX in mind.

Installation
------------

You need to install the following prerequisites in order to use this app::

    pip install Django
    pip install South
    pip install python-dateutil

If you want to install the latest stable release from PyPi::

    $ pip install django-calendarium

If you feel adventurous and want to install the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-calendarium.git#egg=calendarium

Add ``calendarium`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'calendarium',
    )

Run the South migrations::

    ./manage.py migrate calendarium


Usage
-----

TODO: Describe usage


Contribute
----------

If you want to contribute to this project, please perform the following steps::

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 django-calendarium
    $ pip install -r requirements.txt
    $ ./logger/tests/runtests.sh
    # You should get no failing tests

    $ git co -b feature_branch master
    # Implement your feature and tests
    # Describe your change in the CHANGELOG.txt
    $ git add . && git commit
    $ git push origin feature_branch
    # Send us a pull request for your feature branch

Whenever you run the tests a coverage output will be generated in
``tests/coverage/index.html``. When adding new features, please make sure that
you keep the coverage at 100%.


Roadmap
-------

Check the issue tracker on github for milestones and features to come.
