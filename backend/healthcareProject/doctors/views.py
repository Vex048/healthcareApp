from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from patients.models import Patient,MedicalRecord
from .models import Appointment, DLModels, Doctor, ModelResult,Profile,Availability
from django.utils import timezone
from .services.dl_models import pneumonia_model
# Create your views here.
def showDoctors(request):
    doctors = Doctor.objects.all()
    doctors = {'doctors': doctors}
    return render(request, 'doctors/showDoctors.html',doctors)


def doctorProfile(request,id):
    doctor = Doctor.objects.get(id=id)
    profile = Profile.objects.get(doctor_id=id)
    try:
        is_doctor = Doctor.objects.filter(user=request.user).exists()
    except:
        is_doctor = None
    #is_patient = Patient.objects.filter(user=request.user).exists()
    context = {'doctor': doctor,'profile':profile, 'is_doctor': is_doctor}
    return render(request,'doctors/doctorProfile.html',context)

def createAvailability(request,id):
    doctor = Doctor.objects.get(id=id)
    if request.method == "POST":
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        availability = Availability.objects.create(doctor=doctor,date=date,start_time=start_time,end_time=end_time,is_available=True)
        messages.success(request, 'Availability added')
        return redirect('doctor_profile',id=doctor.id)
    context = {'doctor': doctor}
    return render(request,'doctors/createAvailability.html',context)

def doctor_calendar(request,id):
    doctor = Doctor.objects.get(id=id)
    available = Availability.objects.filter(doctor=doctor,date__gte=datetime.now())
    context = {"available":available,"doctor":doctor}
    return render(request,'doctors\showAvailability.html',context)
    

def get_available_times(request,doctor_id,date):
    doctor = Doctor.objects.get(id=doctor_id)
    availability = Availability.objects.filter(doctor=doctor,date=date,is_available=True)
    times = []
    for slot in availability:
        times.append(slot.start_time.strftime('%H:%M'))
    return JsonResponse({'available_times': times})
    
    

def makeAppointment(request,id,slot_id):
    doc = Doctor.objects.get(id=id)
    available = Availability.objects.get(id=slot_id)
    formatted_date = available.date.strftime('%Y-%m-%d')
    start_time = datetime.combine(available.date, available.start_time)
    end_time = datetime.combine(available.date, available.end_time)
    
    available_times = []
    while start_time < end_time:
        available_times.append(start_time.strftime('%H:%M'))
        start_time += timedelta(minutes=60)
        
        
    context = {"doctor":doc,'initial_date':formatted_date,"available_times": available_times }
    if request.method == "POST":
        date = request.POST.get('date')
        time = request.POST.get('time')
        desc = request.POST.get('description')
        Appointment.objects.create(doctor_id=doc,patient_id=request.user.patient,date=date,time=time,description=desc)
        return redirect('home')
    return render(request, 'doctors/makeAppointment.html',context)

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

def listModels(request):
    models = DLModels.objects.all()
    context = {'models':models}
    return render(request,'doctors/DeepLearningModels.html',context)

def model(request,id):
    model = DLModels.objects.get(id=id)
    if request.method == "POST":
        image = request.FILES['image']
        #Proccesing image with model
        img = pneumonia_model.preprocces_image(image)
        prediction = pneumonia_model.predict(img)
        result = pneumonia_model.interpret_result(prediction)
        result = ModelResult.objects.create(model_id=model,result=result,date=datetime.now())
        messages.success(request, 'Result added')
        context = {'model':model,'result':result}
        return render(request,'doctors/models/results.html',context)
    context = {'model':model}
    return render(request,'doctors/models/models_template.html',context)