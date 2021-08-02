"""
This ``urls.py`` is only used when running the tests via ``runtests.py``.
As you know, every app must be hooked into yout main ``urls.py`` so that
you can actually reach the app's views (provided it has any views, of course).

"""
from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin


admin.autodiscover()


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('calendarium.urls')),
]
