from django.contrib import admin

from .models import Event # importuji tridu Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
# Register your models here.
