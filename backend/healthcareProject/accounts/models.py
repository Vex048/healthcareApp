from django.db import models
from django.contrib.auth.models import User
from django import forms
# Create your models here.



class AccountForm(forms.ModelForm):
    first_name = forms.CharField(label="First name", max_length=100)
    last_name = forms.CharField(label="Last name", max_length=100)
    pesel = forms.DecimalField(label="Pesel", max_digits=11)
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())  # Use CharField for passwords

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        
    

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    pesel = models.DecimalField(max_digits=11,decimal_places=0,null=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return self.email
    
    
    