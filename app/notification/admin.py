from django.contrib import admin
from . import models

admin.site.register(models.PushSubscription)
admin.site.register(models.FCMDevice)