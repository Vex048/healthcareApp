from django.db import models

# Create your models here.
class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    about_me = models.TextField(null=True,blank=True)
    experience = models.TextField(null=True)
    graduation = models.TextField(null=True)
    specialization = models.TextField(null=True)
    
    def __str__(self):
        if self.second_name == None:
            return self.first_name + " " + self.last_name
        else:   
            return self.first_name + " " + self.second_name + " "+ self.last_name