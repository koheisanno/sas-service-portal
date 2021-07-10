from django.contrib import admin
from .models import UserProfile, Club, Event, Record, Tag

admin.site.register(UserProfile)
admin.site.register(Club)
admin.site.register(Event)
admin.site.register(Record)
admin.site.register(Tag)