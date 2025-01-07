from django.contrib import admin
from . import models

admin.site.register(models.Clase)
admin.site.register(models.Instructor)
admin.site.register(models.Student)
admin.site.register(models.Tutor)
admin.site.register(models.Atendance)
admin.site.register(models.Announcement)
