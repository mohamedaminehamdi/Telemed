# API URL Configuration for Telemed Backend
# Centralizes all API routes with proper REST conventions

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AppointmentViewSet,
    DoctorViewSet,
    PatientViewSet,
    PrescriptionViewSet,
    ConsultationViewSet
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')
router.register(r'consultations', ConsultationViewSet, basename='consultation')

# API URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
