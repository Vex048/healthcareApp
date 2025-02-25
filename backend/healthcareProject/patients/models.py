from django.db import models
from django.contrib.auth.models import User
from doctors.models import Doctor

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pesel = models.DecimalField(max_digits=11, decimal_places=0)
    def __str__(self):
        return self.user.username

# Create your models here.
class MedicalRecord(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()
    def __str__(self):
        return self.patient.user.username