from django.urls import include, path
from . import views
from doctors.views import doctorProfile

app_name = 'patients'
urlpatterns = [
    # path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    # path('view-records/', views.view_records, name='view_records'),
    path('profile/', views.showPatientProfile, name='profile'),
    path("doctorProfile/<int:id>",doctorProfile,name='doctorProfile'),
    path('view_records/<int:id>', views.view_records, name='view_records'),
    path("view_appoinments/<int:id>",views.view_appointments,name='view_appointments'),
]