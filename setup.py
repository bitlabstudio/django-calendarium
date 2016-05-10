import os
from setuptools import setup, find_packages
import calendarium
try:
    import multiprocessing  # NOQA
except ImportError:
    pass


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name="django-calendarium",
    version=calendarium.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='django, calendar, app, widget, events, schedule',
    author='Daniel Kaufhold',
    author_email='daniel.kaufhold@bitmazk.com',
    url="https://github.com/bitmazk/django-calendarium",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=1.6',
        'python-dateutil',
        'django-filer',
        'django-libs',
    ],
)
