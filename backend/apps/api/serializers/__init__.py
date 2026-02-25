# Backend API Serializers
# This module contains all DRF serializers for the Telemed API

from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with extended fields"""
    
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'is_staff')
        read_only_fields = ('id',)
    
    def get_full_name(self, obj):
        """Get user's full name"""
        return f"{obj.first_name} {obj.last_name}".strip()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password_confirm')
    
    def validate(self, attrs):
        """Validate that passwords match"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': _('Passwords do not match.')
            })
        return attrs
    
    def create(self, validated_data):
        """Create a new user"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class DoctorSerializer(serializers.Serializer):
    """Serializer for Doctor information"""
    
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    specialization = serializers.CharField(max_length=100)
    license_number = serializers.CharField(max_length=50)
    experience_years = serializers.IntegerField()
    phone_number = serializers.CharField(max_length=20)
    is_available = serializers.BooleanField()
    average_rating = serializers.FloatField(read_only=True)


class PatientSerializer(serializers.Serializer):
    """Serializer for Patient information"""
    
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    date_of_birth = serializers.DateField()
    gender = serializers.CharField(max_length=10)
    phone_number = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=255)
    medical_history = serializers.CharField(allow_blank=True)


class AppointmentSerializer(serializers.Serializer):
    """Serializer for Appointment"""
    
    id = serializers.IntegerField(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    scheduled_at = serializers.DateTimeField()
    duration_minutes = serializers.IntegerField(default=30)
    status = serializers.CharField(max_length=20)
    reason = serializers.CharField(max_length=500)
    notes = serializers.CharField(allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)


class PrescriptionSerializer(serializers.Serializer):
    """Serializer for Prescription"""
    
    id = serializers.IntegerField(read_only=True)
    appointment = AppointmentSerializer(read_only=True)
    medication_name = serializers.CharField(max_length=100)
    dosage = serializers.CharField(max_length=100)
    frequency = serializers.CharField(max_length=100)
    duration_days = serializers.IntegerField()
    instructions = serializers.CharField(allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)


class ConsultationSerializer(serializers.Serializer):
    """Serializer for Consultation session"""
    
    id = serializers.IntegerField(read_only=True)
    appointment = AppointmentSerializer(read_only=True)
    video_session_id = serializers.CharField(max_length=100)
    started_at = serializers.DateTimeField()
    ended_at = serializers.DateTimeField(allow_null=True)
    duration_seconds = serializers.IntegerField(read_only=True)
    recording_url = serializers.URLField(allow_blank=True)
    notes = serializers.CharField(allow_blank=True)
