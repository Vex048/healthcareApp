from django.contrib import admin

# Register your models here.
from .models import Doctor,Profile,Appointment,Schedule
admin.site.register(Doctor)
admin.site.register(Profile)
admin.site.register(Appointment)
admin.site.register(Schedule)