from django.contrib import admin

from .models import Choice, Event, EventUser

admin.site.register(Event)
admin.site.register(EventUser)
admin.site.register(Choice)
