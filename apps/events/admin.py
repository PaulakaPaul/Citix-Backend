from django.contrib import admin

from apps.events.models import Event, EventUserReaction


class EventUserReactionAdmin(admin.TabularInline):
    model = EventUserReaction


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')
    inlines = [
        EventUserReactionAdmin,
    ]


admin.site.register(Event, EventAdmin)
