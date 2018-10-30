from django.contrib import admin
from django.utils import timezone
from django.db.models import Count, Q

from .models import Event # importuji tridu Event

# I would like to change a few descriptions
admin.site.site_header = 'Explorea root' # header
admin.site.site_title = 'Explorea root' # card name
admin.site.index_title = 'Select the group' # block title

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    We would like to have an overview of each instance's data on this page.
    """
    # Properties
    list_display = ['host',
                    'truncate_description', 
                    'name',
                    'category',
                    'slug',
                    'events_passed',
                    'events_active',
                    'location',
                    'created',
                    'thumbnail',
                    'main_image'
                    ]
    
    # Easier navigation through lines, thanks to filters
    list_filter = ['category', 'name']
    
    # Another solution for better navigation throughout events
    date_hierarchy = 'created'

    # Enable to search among model's items
    search_fields = ['host__username', 'name', 'location']

    # Faster way how to edit some details
    list_editable = ['category', 'location', 'name']

    def get_queryset(self, request):
        """We will overwrite default ModelAdmin.get_queryset()."""
        qs = super().get_queryset(request)
        qs = qs.annotate(
            events_passed = Count('eventrun',
                filter = Q(eventrun__date__lt=timezone.now())),
            events_future = Count('eventrun',
                filter = Q(eventrun__date__gte=timezone.now()))
        )

        return qs

    def events_passed(self, obj):
        """How many events are basically gone."""
        return obj.events_passed
    # We want to sort our data until they arrived from db
    events_passed.admin_order_field = 'events_passed'

    def events_active(self, obj):
        """How many events will be open in the future."""
        return obj.events_future
    # We want to sort our data until they arrived from db
    events_active.admin_order_field = 'events_future'

    def truncate_description(self, obj):
        """We want to get shorther description."""
        length = 40

        if len(obj.description) > length:
        	return obj.description[:length] + '...'
        elif len(obj.description) < length:
        	return obj.description + '...'
        else:
        	return '--------'
    truncate_description.short_description = 'Description'
