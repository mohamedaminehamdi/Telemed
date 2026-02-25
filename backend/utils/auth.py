# Utility functions for authentication and authorization

from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def is_doctor(user):
    """Check if user is a doctor"""
    return hasattr(user, 'doctor_profile') or user.groups.filter(name='doctors').exists()


def is_patient(user):
    """Check if user is a patient"""
    return hasattr(user, 'patient_profile') or user.groups.filter(name='patients').exists()


def doctor_required(view_func):
    """Decorator to require doctor role"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        if not is_doctor(request.user):
            return Response({'error': 'Doctor role required'}, status=status.HTTP_403_FORBIDDEN)
        return view_func(request, *args, **kwargs)
    return wrapper


def patient_required(view_func):
    """Decorator to require patient role"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        if not is_patient(request.user):
            return Response({'error': 'Patient role required'}, status=status.HTTP_403_FORBIDDEN)
        return view_func(request, *args, **kwargs)
    return wrapper


class RoleBasedAccessControl:
    """Mixin for role-based access control in views"""
    
    def check_doctor_access(self, user):
        """Check if user has doctor access"""
        return is_doctor(user)
    
    def check_patient_access(self, user):
        """Check if user has patient access"""
        return is_patient(user)
    
    def get_user_role(self, user):
        """Get user's primary role"""
        if is_doctor(user):
            return 'doctor'
        elif is_patient(user):
            return 'patient'
        elif user.is_staff:
            return 'admin'
        return 'guest'
