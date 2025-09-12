from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Doctor, Appointment, Availability, DLModels, ModelResult
from .serializers import (
    DoctorSerializer,
    AppointmentSerializer,
    AvailabilitySerializer,
    DLModelsSerializer,
    ModelResultSerializer,
)
import datetime


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__first_name", "user__last_name"]

    def get_queryset(self):
        if (
            self.action in ["update", "partial_update", "destroy"]
            and not self.request.user.is_staff
        ):
            # Only allow doctors to edit their own profile
            if hasattr(self.request.user, "doctor"):
                return Doctor.objects.filter(user=self.request.user)
            return Doctor.objects.none()
        return Doctor.objects.all()  # For list and retrieve, show all doctors

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AvailabilityViewSet(viewsets.ModelViewSet):
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "doctor"):
            # Doctors see only their availabilities
            return Availability.objects.filter(doctor=user.doctor)
        else:
            # Patients see all availabilities for booking
            return Availability.objects.filter(is_available=True)

    def perform_create(self, serializer):
        # Only doctors can create availability
        if hasattr(self.request.user, "doctor"):
            serializer.save(doctor=self.request.user.doctor)
        else:
            raise permissions.PermissionDenied("Only doctors can create availability")


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Base queryset depends on user type
        if hasattr(user, "doctor"):
            queryset = Appointment.objects.filter(doctor_id=user.doctor)
        elif hasattr(user, "patient"):
            queryset = Appointment.objects.filter(patient_id=user.patient)
        else:
            return Appointment.objects.none()

        # Filter by status if provided in query params
        status_filter = self.request.query_params.get("status")
        if status_filter == "upcoming":
            return queryset.filter(date__gte=timezone.now().date()).order_by(
                "date", "time"
            )
        elif status_filter == "past":
            return queryset.filter(date__lt=timezone.now().date()).order_by(
                "-date", "time"
            )

        # Default ordering
        return queryset.order_by("date", "time")

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """Endpoint to cancel an appointment"""
        appointment = self.get_object()

        # Check if the user is associated with this appointment
        user = request.user
        is_owner = (
            hasattr(user, "patient") and appointment.patient_id == user.patient
        ) or (hasattr(user, "doctor") and appointment.doctor_id == user.doctor)

        if not is_owner:
            return Response(
                {"detail": "You don't have permission to cancel this appointment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Can't cancel past appointments
        if appointment.date < timezone.now().date():
            return Response(
                {"detail": "Cannot cancel past appointments."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DLModelsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DLModels.objects.all()
    serializer_class = DLModelsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"])
    def predict(self, request, pk=None):
        """Endpoint for model predictions"""
        model_obj = self.get_object()

        # Handle file upload
        image_file = request.FILES.get("image")
        if not image_file:
            return Response(
                {"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Here you would normally call your model service
        # from services.dl_models import PneunomiaModelService
        # model_service = PneunomiaModelService()
        # result = model_service.predict(image_file)

        # For now, return a placeholder
        result = {"prediction": "Sample prediction", "confidence": 0.95}

        # Save the result
        model_result = ModelResult.objects.create(
            model_id=model_obj, result=str(result), date=timezone.now()
        )

        return Response(
            {"model": model_obj.name, "result": result, "timestamp": model_result.date}
        )


class ModelResultViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ModelResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show results created by current doctor
        if hasattr(self.request.user, "doctor"):
            return ModelResult.objects.filter(
                model_id__created_by=self.request.user.doctor
            )
        return ModelResult.objects.none()
