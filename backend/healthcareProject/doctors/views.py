from django.shortcuts import render
from .models import Doctor
# Create your views here.
def showDoctors(request):
    doctors = Doctor.objects.all()
    doctors = {'doctors': doctors}
    return render(request, 'doctors/showDoctors.html',doctors)