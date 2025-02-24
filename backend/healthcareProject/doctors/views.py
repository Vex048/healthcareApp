from django.shortcuts import render
from .models import Doctor,Profile
# Create your views here.
def showDoctors(request):
    doctors = Doctor.objects.all()
    doctors = {'doctors': doctors}
    return render(request, 'doctors/showDoctors.html',doctors)


def doctorProfile(request,id):
    doctor = Doctor.objects.get(id=id)
    profile = Profile.objects.get(doctor_id=id)
    context = {'doctor': doctor,'profile':profile}
    return render(request,'doctors/doctorProfile.html',context)

def makeAppointment(request,id):
    return render(request, 'doctors/makeAppointment.html')