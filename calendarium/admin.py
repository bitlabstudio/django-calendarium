"""Admin views for the models of the ``calendarium`` app."""
from django.contrib import admin

from calendarium.models import (
    Event,
    EventCategory,
    EventRelation,
    Occurrence,
    Rule,
)


class EventAdmin(admin.ModelAdmin):
    """Custom admin for the ``Event`` model."""
    model = Event
    fields = (
        'title', 'start', 'end', 'description', 'category', 'created_by',
        'rule', 'end_recurring_period', )
    list_display = (
        'title', 'start', 'end', 'category', 'created_by', 'rule',
        'end_recurring_period', )
    search_fields = ('title', 'description', )
    date_hierarchy = 'start'
    list_filter = ('category', )


class EventCategoryAdmin(admin.ModelAdmin):
    """Custom admin to display a small colored square."""
    model = EventCategory
    list_display = ('name', 'color', )
    list_editable = ('color', )


admin.site.register(Event, EventAdmin)
admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(EventRelation)
admin.site.register(Occurrence)
admin.site.register(Rule)
