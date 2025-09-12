from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"profiles", views.PatientViewSet, basename="patient")
router.register(r"records", views.MedicalRecordViewSet, basename="medicalrecord")

app_name = "patients"

urlpatterns = [
    path("", include(router.urls)),
]
