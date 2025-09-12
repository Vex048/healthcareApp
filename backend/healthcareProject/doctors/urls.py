from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"profiles", views.DoctorViewSet, basename="doctor")
router.register(r"appointments", views.AppointmentViewSet, basename="appointment")
router.register(r"availability", views.AvailabilityViewSet, basename="availability")
router.register(r"models", views.DLModelsViewSet, basename="dlmodels")
router.register(r"results", views.ModelResultViewSet, basename="modelresults")

app_name = "doctors"

urlpatterns = [
    path("", include(router.urls)),
]
