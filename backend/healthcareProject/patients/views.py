from rest_framework import viewsets, permissions
from .models import Patient, MedicalRecord
from .serializers import PatientSerializer, MedicalRecordSerializer


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Patients can only see their own profile
        if hasattr(user, "patient"):
            return Patient.objects.filter(user=user)

        # Doctors can see patients they have appointments with
        elif hasattr(user, "doctor"):
            from doctors.models import Appointment

            patient_ids = (
                Appointment.objects.filter(doctor_id=user.doctor)
                .values_list("patient_id", flat=True)
                .distinct()
            )
            return Patient.objects.filter(id__in=patient_ids)

        # Admin can see all
        elif user.is_staff:
            return Patient.objects.all()

        return Patient.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MedicalRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Patients can only see their own records
        if hasattr(user, "patient"):
            return MedicalRecord.objects.filter(patient=user.patient)

        # Doctors can see records they created
        elif hasattr(user, "doctor"):
            return MedicalRecord.objects.filter(doctor=user.doctor)

        # Admin can see all
        elif user.is_staff:
            return MedicalRecord.objects.all()

        return MedicalRecord.objects.none()

    def perform_create(self, serializer):
        if hasattr(self.request.user, "doctor"):
            serializer.save(doctor=self.request.user.doctor)
        else:
            raise permissions.PermissionDenied(
                "Only doctors can create medical records"
            )
