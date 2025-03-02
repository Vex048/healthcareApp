from django.shortcuts import render

from patients.models import Patient,MedicalRecord
from .models import Appointment, Doctor,Profile
# Create your views here.
def showDoctors(request):
    doctors = Doctor.objects.all()
    doctors = {'doctors': doctors}
    return render(request, 'doctors/showDoctors.html',doctors)


def doctorProfile(request,id):
    doctor = Doctor.objects.get(id=id)
    profile = Profile.objects.get(doctor_id=id)
    is_doctor = Doctor.objects.filter(user=request.user).exists()
    #is_patient = Patient.objects.filter(user=request.user).exists()
    context = {'doctor': doctor,'profile':profile, 'is_doctor': is_doctor}
    return render(request,'doctors/doctorProfile.html',context)

def makeAppointment(request,id):
    if request.method == "POST":
        date = request.POST.get('date')
        time = request.POST.get('time')
        desc = request.POST.get('description')
        doc = Doctor.objects.get(id=id)
        Appointment.objects.create(doctor_id=doc,patient_id=request.user.patient,date=date,time=time,description=desc)
        return render(request, 'doctors/makeAppointment.html')
    return render(request, 'doctors/makeAppointment.html')

def createReport(request):
    if request.method == "POST":
        date = request.POST.get('date')
        desc = request.POST.get('description')
        patient = request.POST.get('patient')
        patient = Patient.objects.get(user__username=patient)
        doc = Doctor.objects.get(user=request.user)
        MedicalRecord.objects.create(doctor=doc,patient=patient,date=date,description=desc)
        return render(request, 'doctors/createReport.html')
    patients= Patient.objects.all()
    context = {"patients":patients}
    return render(request, 'doctors/createReport.html',context)