flake8 --ignore=E126 --statistics --exclude=submodules,migrations,node_modules --snippets="import ipdb,ipdb.set_trace()" .
coverage run --source='.' manage.py test -v 2 --traceback --failfast --pattern='*_tests.py'
coverage html -d calendarium/tests/coverage --omit="'*__init__*,*manage*,*wsgi*,*urls*,*/settings/*,*/migrations/*,*/south_migrations/*,*/tests/*,*admin*'"