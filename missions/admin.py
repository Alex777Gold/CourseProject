from django.contrib import admin
from .models import Mission, Subscription, MissionDetail

admin.site.register(Mission)
admin.site.register(MissionDetail)
admin.site.register(Subscription)
