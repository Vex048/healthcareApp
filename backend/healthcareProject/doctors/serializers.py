from rest_framework import serializers
from .models import Doctor, Appointment, Availability, DLModels, ModelResult
from accounts.serializers import UserSerializer


class DoctorSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Doctor
        fields = [
            "id",
            "user",
            "user_details",
            "first_name",
            "second_name",
            "last_name",
            "email",
        ]
        read_only_fields = ["user"]


class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.ReadOnlyField(source="doctor_id.user.get_full_name")
    patient_name = serializers.ReadOnlyField(source="patient_id.user.get_full_name")

    class Meta:
        model = Appointment
        fields = [
            "id",
            "doctor_id",
            "patient_id",
            "doctor_name",
            "patient_name",
            "date",
            "time",
            "description",
        ]


class AvailabilitySerializer(serializers.ModelSerializer):
    doctor_name = serializers.ReadOnlyField(source="doctor.user.get_full_name")

    class Meta:
        model = Availability
        fields = [
            "id",
            "doctor",
            "doctor_name",
            "date",
            "start_time",
            "end_time",
            "is_available",
        ]
        read_only_fields = ["doctor"]


class DLModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DLModels
        fields = "__all__"


class ModelResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelResult
        fields = "__all__"
