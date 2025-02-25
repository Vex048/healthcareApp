from django.shortcuts import render
from .models import MedicalRecord
# Create your views here.
def showPatientProfile(request):
    try:
        medical_record = MedicalRecord.objects.get(patient=request.user.patient)
    except:
        medical_record = None
    context = {'medical_record': medical_record}
    return render(request, 'patients/profile.html',context)
