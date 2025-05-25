from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from patients.models import Patient,MedicalRecord
from .models import Appointment, DLModels, Doctor, ModelResult,Profile,Availability
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .services.dl_models import pneumonia_model

def showDoctors(request):
    doctors = Doctor.objects.all()
    doctors = {'doctors': doctors}
    return render(request, 'doctors/showDoctors.html',doctors)


def doctorProfile(request,id):
    try:
        doctor = Doctor.objects.get(id=id)
        profile = Profile.objects.get(doctor_id=id)
    
        try:
            is_doctor = Doctor.objects.filter(user=request.user).exists()
        except:
            is_doctor = None
        context = {'doctor': doctor,'profile':profile, 'is_doctor': is_doctor}
        return render(request,'doctors/doctorProfile.html',context)
    except Doctor.DoesNotExist:
        messages.error("The doctor_id is invalid, doctor not found")
        return redirect('home')
    except Profile.DoesNotExist:
        messages.error("The profile does not exist")
        return redirect('home')

@login_required
def createAvailability(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.error("Doctor doestn exist")
        return redirect('home')
    available_days = Availability.objects.filter(doctor=doctor,date__gte=datetime.now())
    if request.method == "POST":
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        if not all([date, start_time, end_time]):
                messages.error(request, "You have to fill all of the fields")
                context = {'available': available_days, 'doctor': doctor}
                return render(request, 'doctors/createAvailability.html', context)
        Availability.objects.create(doctor=doctor,date=date,start_time=start_time,end_time=end_time,is_available=True)
        messages.success(request, 'Availability added')
        return redirect('doctors:doctorProfile',id=doctor.id)
    context = {'available': available_days,'doctor':doctor}
    return render(request,'doctors/createAvailability.html',context)

def doctor_calendar(request,id):
    try:
        doctor = Doctor.objects.get(id=id)
    except Doctor.DoesNotExist:
        messages.error("Doctor dose not exist")
        return redirect('home')
    available = Availability.objects.filter(doctor=doctor,date__gte=datetime.now())
    context = {"available":available,"doctor":doctor}
    return render(request,'doctors/showAvailability.html',context)
    

def get_time_slots(doctor,date_string):
    date = datetime.strptime(date_string,'%Y-%m-%d').date()
    availability = Availability.objects.get(doctor=doctor,date=date,is_available=True)
    start_time = datetime.combine(availability.date, availability.start_time)
    end_time = datetime.combine(availability.date, availability.end_time)
    formatted_date = date.strftime('%Y-%m-%d')
    
    all_appointments_day = Appointment.objects.filter(doctor_id=doctor,date=formatted_date).values_list('time',flat=True)
    booked_times=[]
    for appointment_time in all_appointments_day:
        if hasattr(appointment_time, 'strftime'):
            booked_times.append(appointment_time.strftime('%H:%M'))
        else:
            booked_times.append(appointment_time)
    available_times = []
    while start_time < end_time:
        curr_time = start_time.strftime('%H:%M')
        if curr_time not in booked_times:    
            available_times.append(curr_time)
        start_time += timedelta(minutes=60)
    return available_times


# API Endpoint
# def get_available_times(request,doctor_id,date):
#     doctor = Doctor.objects.get(id=doctor_id)
#     times = get_time_slots(doctor,str(date))
#     return JsonResponse({'available_times': times})
    
    
@login_required
def makeAppointment(request,id,slot_id):
    doc = Doctor.objects.get(id=id)
    available = Availability.objects.get(id=slot_id)
    formatted_date = available.date.strftime('%Y-%m-%d')
    available_times = get_time_slots(doc,formatted_date)
        
        
    context = {"doctor":doc,'initial_date':formatted_date,"available_times": available_times }
    if request.method == "POST":
        date = request.POST.get('date')
        time = request.POST.get('time')
        desc = request.POST.get('description')
        Appointment.objects.create(doctor_id=doc,patient_id=request.user.patient,date=date,time=time,description=desc)
        return redirect('home')
    return render(request, 'doctors/makeAppointment.html',context)

@login_required
def createReport(request):
    if request.method == "POST":
        date = request.POST.get('date')
        desc = request.POST.get('description')
        patient = request.POST.get('patient')
        patient = Patient.objects.get(user__username=patient)
        doc = Doctor.objects.get(user=request.user)
        MedicalRecord.objects.create(doctor=doc,patient=patient,date=date,description=desc)
        return render(request, 'doctors/createReport.html')
    #patients = Appointment.objects.filter(doctor_id = request.user.doctor).values_list('patient_id',flat=True)
    appointments = Appointment.objects.filter(doctor_id = request.user.doctor).values_list('patient_id',flat=True)
    
    patients= Patient.objects.filter(id__in=appointments)
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