from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account
from dj_rest_auth.registration.serializers import RegisterSerializer


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        read_only_fields = ["user"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        read_only_fields = ["id", "email", "username"]


class CustomRegisterSerializer(RegisterSerializer):
    user_type = serializers.ChoiceField(
        choices=[("patient", "Patient"), ("doctor", "Doctor")]
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get("first_name", "")
        user.last_name = self.validated_data.get("last_name", "")
        user.save()

        from patients.models import Patient
        from doctors.models import Doctor

        # Create appropriate profile based on user_type
        user_type = self.validated_data.get("user_type", "patient")
        if user_type == "patient":
            Patient.objects.create(user=user)
        elif user_type == "doctor":
            Doctor.objects.create(user=user)
