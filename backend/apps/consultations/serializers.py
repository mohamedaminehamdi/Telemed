# Video Consultation Models and Logic

from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class VideoConsultationSerializer(serializers.Serializer):
    """Serializer for video consultation sessions"""
    
    id = serializers.IntegerField(read_only=True)
    appointment_id = serializers.IntegerField()
    video_session_id = serializers.CharField(max_length=100)
    participant_doctor = serializers.CharField(max_length=100)
    participant_patient = serializers.CharField(max_length=100)
    started_at = serializers.DateTimeField(read_only=True)
    ended_at = serializers.DateTimeField(allow_null=True)
    duration_seconds = serializers.IntegerField(read_only=True)
    recording_url = serializers.URLField(allow_blank=True)
    recording_status = serializers.CharField(max_length=20, default='pending')
    session_notes = serializers.CharField(allow_blank=True)
    is_active = serializers.BooleanField(read_only=True)


class VideoConsultationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing video consultations
    
    Supports:
    - Create video consultation session
    - Start/end consultation
    - Upload recording
    - Get consultation history
    """
    
    serializer_class = VideoConsultationSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def start_session(self, request):
        """Start a new video consultation"""
        appointment_id = request.data.get('appointment_id')
        
        if not appointment_id:
            return Response(
                {'error': 'appointment_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate video session
        import secrets
        video_session_id = secrets.token_urlsafe(12)
        
        consultation_data = {
            'appointment_id': appointment_id,
            'video_session_id': video_session_id,
            'participant_doctor': request.user.email,
            'started_at': __import__('django.utils.timezone', fromlist=['now']).now(),
        }
        
        # Create or update consultation in database
        # Return room details for video SDK
        return Response({
            'video_session_id': video_session_id,
            'room_id': f"telemed-{video_session_id}",
            'token': __import__('secrets', fromlist=['token_urlsafe']).token_urlsafe(32),
            'server_url': 'https://jitsi.example.com',
            'conference_name': f"appointment-{appointment_id}",
        })
    
    @action(detail=False, methods=['post'])
    def end_session(self, request):
        """End an ongoing video consultation"""
        video_session_id = request.data.get('video_session_id')
        session_notes = request.data.get('session_notes', '')
        
        if not video_session_id:
            return Response(
                {'error': 'video_session_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update consultation end time and notes
        # Calculate duration
        duration_seconds = __import__('time').time()  # Placeholder
        
        return Response({
            'status': 'consultation ended',
            'session_id': video_session_id,
            'duration_seconds': duration_seconds,
            'recording_id': 'rec_' + __import__('secrets', fromlist=['token_urlsafe']).token_urlsafe(12),
        })
    
    @action(detail=False, methods=['post'])
    def upload_recording(self, request):
        """Handle recording upload"""
        video_session_id = request.data.get('video_session_id')
        recording_file = request.FILES.get('recording')
        
        if not video_session_id or not recording_file:
            return Response(
                {'error': 'video_session_id and recording file are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Save recording to storage (S3, GCS, or local)
        import os
        recording_id = __import__('secrets', fromlist=['token_urlsafe']).token_urlsafe(12)
        
        return Response({
            'status': 'recording uploaded',
            'recording_id': recording_id,
            'recording_url': f"https://storage.example.com/recordings/{recording_id}",
            'file_size': recording_file.size,
            'duration_seconds': 0,  # Extract from file metadata
        })
    
    @action(detail=False, methods=['get'])
    def get_active_session(self, request):
        """Get currently active consultation session"""
        appointment_id = request.query_params.get('appointment_id')
        
        # Fetch active session
        return Response({
            'session_active': True,
            'video_session_id': 'session_abc123',
            'started_at': __import__('django.utils.timezone', fromlist=['now']).now(),
            'participants': [
                {'name': 'Dr. John Smith', 'type': 'doctor', 'audio_on': True, 'video_on': True},
                {'name': 'Jane Doe', 'type': 'patient', 'audio_on': True, 'video_on': True},
            ]
        })
    
    @action(detail=False, methods=['get'])
    def get_session_history(self, request):
        """Get consultation history for user"""
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 10)

        # Fetch consultation history
        consultations = [
            {
                'id': 1,
                'appointment_id': 1,
                'doctor': 'Dr. Smith',
                'patient': 'Jane Doe',
                'started_at': '2026-02-15T10:00:00Z',
                'duration_seconds': 1800,
                'recording_url': 'https://storage.example.com/recordings/rec_abc',
            }
        ]
        
        return Response({
            'count': len(consultations),
            'results': consultations,
        })
