"""Admin views for the models of the ``calendarium`` app."""
from django.contrib import admin

from calendarium.models import (
    Event,
    EventCategory,
    EventRelation,
    Occurrence,
    Rule,
)


class EventCategoryAdmin(admin.ModelAdmin):
    """Custom admin to display a small colored square."""
    model = EventCategory
    list_display = ('name', 'color', )
    list_editable = ('color', )


admin.site.register(Event)
admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(EventRelation)
admin.site.register(Occurrence)
admin.site.register(Rule)
