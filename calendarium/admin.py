"""Admin views for the models of the ``calendarium`` app."""
from django.contrib import admin

from calendarium.models import (
    Event,
    EventCategory,
    EventRelation,
    Occurrence,
    Rule,
)


admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(EventRelation)
admin.site.register(Occurrence)
admin.site.register(Rule)
