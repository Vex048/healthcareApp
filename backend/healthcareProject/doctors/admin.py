from django.contrib import admin

# Register your models here.
from .models import DLModels, Doctor,Profile,Appointment,Schedule,Availability
admin.site.register(Doctor)
admin.site.register(Profile)
admin.site.register(Appointment)
admin.site.register(Schedule)
admin.site.register(DLModels)
admin.site.register(Availability)