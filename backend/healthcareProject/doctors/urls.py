from django.urls import path
from . import views
app_name = 'doctors'
urlpatterns = [
    # path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    # path('upload-image/', views.upload_image, name='upload_image'),
    path('showDoctors/', views.showDoctors, name='showDoctors'),
    path("doctorProfile/<int:id>",views.doctorProfile,name='doctorProfile'),
    path("makeAppointment/<int:id>",views.makeAppointment,name='makeAppointment'),
    path("createReport/",views.createReport,name='createReport'),
    path("listModels/",views.listModels,name='listModels'),
    path("model/<int:id>",views.model,name='model'),
]