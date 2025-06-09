import datetime
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from doctors.models import Appointment, Doctor, Profile
from .models import MedicalRecord, Patient
from django.contrib import messages
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


def cancel_appointment(request,appointment_id):
    if request.method == "POST":
        appointment = Appointment.objects.get(id=appointment_id)
        if appointment.patient_id.user != request.user:
            messages.error(request, "You can only cancel your own appointments")
        else:
            try:
                appointment.delete()
                messages.success(request,"Succesfully deletaed appointment")
            except:
                messages.error(request,"There was a problem with deleting appointment")
        patient_id = request.user.patient.id
        return redirect('patients:view_appointments',id=patient_id)
        
     
    

def view_appointments(request,id): 
    patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient_id=patient)
    context = {'appointments': appointments,'today': timezone.now().date()}
    return render(request, 'patients/appointments.html',context)
    

def render_chatbot(request):
    return render(request,'patients/chatbot.html')