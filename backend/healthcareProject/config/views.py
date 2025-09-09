from datetime import datetime
from django.shortcuts import render

from doctors.models import Appointment, Doctor

def home(request):
    context = {}
    
    if request.user.is_authenticated:
        if hasattr(request.user, 'doctor'):
            # For doctors
            doctor = request.user.doctor
            today = datetime.now().date()
            
            # Get today's appointments
            today_appointments = Appointment.objects.filter(
                doctor_id=doctor,
                date=today
            ).order_by('time')
            
            # Get upcoming appointments
            upcoming_appointments = Appointment.objects.filter(
                doctor_id=doctor,
                date__gte=today
            ).order_by('date', 'time')[:5]
            
            # Count total unique patients
            total_patients = Appointment.objects.filter(
                doctor_id=doctor
            ).values('patient_id').distinct().count()
            
            context.update({
                'today_appointments': today_appointments,
                'upcoming_appointments': upcoming_appointments,
                'total_patients': total_patients
            })
        else:
            # For patients
            if hasattr(request.user, 'patient'):
                patient = request.user.patient
                today = datetime.now().date()
                
                # Get upcoming appointments
                upcoming_appointments = Appointment.objects.filter(
                    patient_id=patient,
                    date__gte=today
                ).order_by('date', 'time')
                
                # Get featured doctors (example: showing 3 random doctors)
                featured_doctors = Doctor.objects.all().order_by('?')[:3]
                
                context.update({
                    'upcoming_appointments': upcoming_appointments,
                    'featured_doctors': featured_doctors
                })
    
    return render(request, 'home.html', context)