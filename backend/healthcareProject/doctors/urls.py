from django.urls import path
from . import views
app_name = 'doctors'
urlpatterns = [
    # path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    # path('upload-image/', views.upload_image, name='upload_image'),
    path('showDoctors/', views.showDoctors, name='showDoctors'),
    path("doctorProfile/<int:id>",views.doctorProfile,name='doctorProfile'),
    path("makeAppointment/<int:id>/<int:slot_id>",views.makeAppointment,name='makeAppointment'),
    path("createReport/",views.createReport,name='createReport'),
    path("listModels/",views.listModels,name='listModels'),
    path("model/<int:id>",views.model,name='model'),
    path("doctor_calendar/<int:id>",views.doctor_calendar,name="doctor_calendar"),
    #path('doctor/<int:doctor_id>/available-times/<str:date>/', views.get_available_times, name='get_available_times'),
    path('create_availability/', views.createAvailability, name='createAvailability'),
    path('delete_availability/<int:availability_id>/', views.delete_availability, name='delete_availability'),
    path('manage_availabilities',views.manage_availability,name='manage_availability')
]