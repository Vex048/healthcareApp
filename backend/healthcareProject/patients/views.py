from django.shortcuts import render

from doctors.models import Appointment
from .models import MedicalRecord
# Create your views here.
def showPatientProfile(request):
    try:
        medical_record = MedicalRecord.objects.filter(patient=request.user.patient)
    except:
        medical_record = None
    try:
        appointments = Appointment.objects.filter(patient_id=request.user.patient)
    except:
        appointments = None
    context = {'medical_record': medical_record,"appointments":appointments}
    return render(request, 'patients/profile.html',context)
