from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        if self.second_name == None:
            return self.first_name + " " + self.last_name
        else:   
            return self.first_name + " " + self.second_name + " "+ self.last_name
class Profile(models.Model):
    doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    about_me = models.TextField(null=True,blank=True)
    experience = models.TextField(null=True)
    graduation = models.TextField(null=True)
    specialization = models.TextField(null=True)


class Schedule(models.Model):
    doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    day=models.CharField(max_length=100)
    start_time=models.TimeField()
    end_time=models.TimeField()
    def __str__(self):
        return self.doctor_id.first_name + " " + self.doctor_id.last_name + " " + self.day + " " + str(self.start_time) + " " + str(self.end_time)
    
class Availability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="availability_slots")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.doctor.user.get_full_name()} - {self.date} ({self.start_time} to {self.end_time})"
    
    
class Appointment(models.Model):
    doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient_id=models.ForeignKey('patients.Patient',on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()
    description=models.TextField(null=True,blank=True)
    def __str__(self):
        return self.doctor_id.first_name + " " + self.doctor_id.last_name + " " + self.patient_id.user.username + " " + str(self.date) + " " + str(self.time)
    
class DLModels(models.Model):
    model = models.FileField(upload_to='models/',null=True,blank=True)
    type = models.TextField(null=True,blank=True)
    descritpion = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.type
class ModelResult(models.Model):
    model_id=models.ForeignKey(DLModels,on_delete=models.CASCADE)
    result=models.TextField()
    date=models.DateField()
    def __str__(self):
        return self.model_id.type + " " + str(self.date)