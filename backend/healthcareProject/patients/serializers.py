from rest_framework import serializers
from .models import Patient, MedicalRecord
from accounts.serializers import UserSerializer


class PatientSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Patient
        fields = ["id", "user", "user_details", "pesel"]
        read_only_fields = ["user"]


class MedicalRecordSerializer(serializers.ModelSerializer):
    doctor_name = serializers.ReadOnlyField(source="doctor.user.get_full_name")
    patient_name = serializers.ReadOnlyField(source="patient.user.get_full_name")

    class Meta:
        model = MedicalRecord
        fields = [
            "id",
            "patient",
            "doctor",
            "patient_name",
            "doctor_name",
            "date",
            "description",
        ]
        read_only_fields = ["doctor"]
