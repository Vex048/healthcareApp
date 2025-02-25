from django.urls import path
from . import views

app_name = 'patients'
urlpatterns = [
    # path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    # path('view-records/', views.view_records, name='view_records'),
    path('profile/', views.showPatientProfile, name='profile'),
]