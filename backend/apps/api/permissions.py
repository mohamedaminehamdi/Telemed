# Role-Based Permissions for API endpoints

from rest_framework.permissions import BasePermission


class IsDoctor(BasePermission):
    """Permission to check if user is a doctor"""
    
    message = 'Only doctors can access this endpoint.'
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'doctor_profile')


class IsPatient(BasePermission):
    """Permission to check if user is a patient"""
    
    message = 'Only patients can access this endpoint.'
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'patient_profile')


class IsOwner(BasePermission):
    """Permission to check if user is the object owner"""
    
    message = 'You do not have permission to access this resource.'
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user


class IsDoctorOrReadOnly(BasePermission):
    """Permission to allow doctors to edit, others can only read"""
    
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_authenticated and hasattr(request.user, 'doctor_profile')


class IsPatientOrReadOnly(BasePermission):
    """Permission to allow patients to edit, others can only read"""
    
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_authenticated and hasattr(request.user, 'patient_profile')


class CanAccessAppointment(BasePermission):
    """Permission to check if user can access an appointment"""
    
    message = 'You do not have permission to access this appointment.'
    
    def has_object_permission(self, request, view, obj):
        # Doctor can access if it's their appointment
        if hasattr(request.user, 'doctor_profile'):
            return obj.doctor.user == request.user
        # Patient can access if it's their appointment
        if hasattr(request.user, 'patient_profile'):
            return obj.patient.user == request.user
        # Admin can access everything
        return request.user.is_staff


class CanAccessConsultation(BasePermission):
    """Permission to check if user can access a consultation"""
    
    message = 'You do not have permission to access this consultation.'
    
    def has_object_permission(self, request, view, obj):
        appointment = obj.appointment
        if hasattr(request.user, 'doctor_profile'):
            return appointment.doctor.user == request.user
        if hasattr(request.user, 'patient_profile'):
            return appointment.patient.user == request.user
        return request.user.is_staff
