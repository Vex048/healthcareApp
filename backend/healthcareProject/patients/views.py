import datetime
from django.shortcuts import redirect, render
from django.urls import reverse

from doctors.models import Appointment, Doctor, Profile
from .models import MedicalRecord, Patient
# Create your views here.
def showPatientProfile(request):
    is_doctor = Doctor.objects.filter(user=request.user).exists()
    if is_doctor:
        doc_id = Doctor.objects.get(user=request.user).id
        return redirect(reverse('doctors:doctorProfile', args=[doc_id]))
    else:      
        try:
            medical_record = MedicalRecord.objects.filter(patient=request.user.patient)
        except:
            medical_record = None
        try:
            appointments = Appointment.objects.filter(patient_id=request.user.patient).filter(date__gte=datetime.date.today())
        except:
            appointments = None
        context = {'medical_record': medical_record,"appointments":appointments}
        return render(request, 'patients/profile.html',context)


def view_records(request,id):
    patient = Patient.objects.get(user=request.user)
    medical_record = MedicalRecord.objects.filter(patient=patient)
    context = {'medical_record': medical_record}
    return render(request, 'patients/medicalReport.html',context)


def upcomingAppointmets(request):
    patient = Patient.objects.get(user=request.user)
    
    

def view_appointments(request,id):
    patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient_id=patient)
    context = {'appointments': appointments}
    return render(request, 'patients/appointments.html',context)
    
