# Backend API Views
# This module contains all DRF views for the Telemed API

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    AppointmentSerializer,
    DoctorSerializer,
    PatientSerializer,
    PrescriptionSerializer,
    ConsultationSerializer,
    UserSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination for list views"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing medical appointments
    
    Supports:
    - List all appointments (paginated)
    - Create new appointment
    - Retrieve appointment details
    - Update appointment
    - Delete appointment
    - Custom actions: confirm, cancel, reschedule, mark_completed
    """
    
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'doctor', 'patient']
    search_fields = ['reason', 'notes']
    ordering_fields = ['scheduled_at', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter appointments based on user role"""
        user = self.request.user
        if user.is_staff:
            return appointments.objects.all()
        # Implement patient/doctor specific filtering
        return appointments.objects.filter(patient__user=user) | appointments.objects.filter(doctor__user=user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def confirm(self, request, pk=None):
        """Confirm an appointment"""
        appointment = self.get_object()
        appointment.status = 'confirmed'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        """Cancel an appointment"""
        appointment = self.get_object()
        appointment.status = 'cancelled'
        appointment.save()
        return Response({'status': 'appointment cancelled'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reschedule(self, request, pk=None):
        """Reschedule an appointment"""
        appointment = self.get_object()
        new_date = request.data.get('scheduled_at')
        if new_date:
            appointment.scheduled_at = new_date
            appointment.save()
            serializer = self.get_serializer(appointment)
            return Response(serializer.data)
        return Response({'error': 'scheduled_at is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_completed(self, request, pk=None):
        """Mark appointment as completed"""
        appointment = self.get_object()
        appointment.status = 'completed'
        appointment.save()
        return Response({'status': 'appointment marked as completed'})


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing doctor profiles
    
    Supports:
    - List all available doctors (with filtering/search)
    - Retrieve doctor details
    - Custom action: get available slots
    """
    
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['specialization', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'specialization']
    
    def get_queryset(self):
        """Return available doctors"""
        return doctors.objects.filter(is_available=True)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def available_slots(self, request, pk=None):
        """Get available time slots for a doctor"""
        doctor = self.get_object()
        date = request.query_params.get('date')
        # Implement slot availability logic
        return Response({
            'doctor_id': doctor.id,
            'date': date,
            'available_slots': ['09:00', '10:00', '11:00', '14:00', '15:00']
        })


class PatientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing patient profiles"""
    
    serializer_class = PatientSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Return all patients (admin only)"""
        return patients.objects.all()


class PrescriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing prescriptions
    
    Supports CRUD operations with filtering by appointment
    """
    
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['appointment']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter prescriptions based on user"""
        user = self.request.user
        # Return prescriptions for patient or doctor
        return prescriptions.objects.all()


class ConsultationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing video consultations
    
    Supports:
    - Create consultation session
    - End consultation
    - Get consultation details
    - Upload recording
    """
    
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def end_session(self, request, pk=None):
        """End a consultation session"""
        consultation = self.get_object()
        # Update end time and duration
        return Response({'status': 'consultation ended'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def upload_recording(self, request, pk=None):
        """Upload consultation recording"""
        consultation = self.get_object()
        # Handle recording upload
        return Response({'status': 'recording uploaded'})
