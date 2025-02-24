from django.db import models


# Create your models here.
class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    
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
    
class Appointment(models.Model):
    doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient_id=models.ForeignKey('patients.Patient',on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()
    def __str__(self):
        return self.doctor_id.first_name + " " + self.doctor_id.last_name + " " + self.patient_id.user.username + " " + str(self.date) + " " + str(self.time)