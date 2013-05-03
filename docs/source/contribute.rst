Contribute
==========

If you want to contribute to this project, please perform the following steps::

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 django-calendarium
    $ pip install -r requirements.txt
    $ python setup.py test
    # You should get no failing tests

    $ git checkout -b feature_branch master
    # Implement your feature and tests
    # Describe your change in the CHANGELOG.txt
    $ git add . && git commit
    $ git push -u origin HEAD
    # Send us a pull request for your feature branch

Whenever you run the tests a coverage output will be generated in
``calendarium/tests/coverage/index.html``. When adding new features, please
make sure that you keep the coverage at 100%.
