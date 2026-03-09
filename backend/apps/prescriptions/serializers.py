# Prescription Management Models and Serializers

from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta


class MedicationSerializer(serializers.Serializer):
    """Serializer for medication information"""
    
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    generic_name = serializers.CharField(max_length=100, allow_blank=True)
    description = serializers.CharField(allow_blank=True)
    warnings = serializers.CharField(allow_blank=True)
    side_effects = serializers.ListField(child=serializers.CharField())


class PrescriptionSerializer(serializers.Serializer):
    """Serializer for medical prescriptions"""
    
    id = serializers.IntegerField(read_only=True)
    appointment_id = serializers.IntegerField()
    doctor_id = serializers.IntegerField(read_only=True)
    patient_id = serializers.IntegerField(read_only=True)
    medication_name = serializers.CharField(max_length=100)
    dosage = serializers.CharField(max_length=100)
    frequency = serializers.CharField(max_length=100)
    duration_days = serializers.IntegerField()
    quantity = serializers.IntegerField()
    refills_allowed = serializers.IntegerField(default=0)
    instructions = serializers.CharField(allow_blank=True)
    warnings = serializers.CharField(allow_blank=True)
    interactions = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    status = serializers.CharField(max_length=20, default='active')
    created_at = serializers.DateTimeField(read_only=True)
    expires_at = serializers.DateTimeField(read_only=True)
    is_controlled = serializers.BooleanField(default=False)


class PrescriptionHistorySerializer(serializers.Serializer):
    """Serializer for prescription history"""
    
    id = serializers.IntegerField(read_only=True)
    prescription_id = serializers.IntegerField()
    action = serializers.CharField(max_length=50)
    action_by = serializers.CharField(max_length=100)
    timestamp = serializers.DateTimeField(read_only=True)
    notes = serializers.CharField(allow_blank=True)


class PrescriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing medical prescriptions
    
    Supports:
    - Create prescriptions
    - View prescriptions (filtered by patient/doctor)
    - Update prescriptions
    - Refill prescriptions
    - Validate drug interactions
    - Export prescriptions (PDF, HL7)
    """
    
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def my_prescriptions(self, request):
        """Get prescriptions for current user"""
        user_type = request.query_params.get('type')  # 'doctor' or 'patient'
        page = request.query_params.get('page', 1)
        page_size = int(request.query_params.get('page_size', 10))
        
        # Mock data
        prescriptions = [
            {
                'id': 1,
                'medication_name': 'Aspirin',
                'dosage': '500mg',
                'frequency': 'twice daily',
                'duration_days': 7,
                'status': 'active'
            },
            {
                'id': 2,
                'medication_name': 'Ibuprofen',
                'dosage': '200mg',
                'frequency': 'three times daily',
                'duration_days': 10,
                'status': 'active'
            }
        ]
        
        return Response({
            'count': len(prescriptions),
            'page': page,
            'page_size': page_size,
            'results': prescriptions
        })
    
    @action(detail=True, methods=['post'])
    def refill(self, request, pk=None):
        """Request a prescription refill"""
        prescription = {'id': pk}
        refill_count = request.data.get('refill_count', 1)
        reason = request.data.get('reason', '')
        
        return Response({
            'status': 'refill_requested',
            'prescription_id': pk,
            'refill_count': refill_count,
            'expires_at': (datetime.now() + timedelta(days=30)).isoformat()
        })
    
    @action(detail=True, methods=['post'])
    def approve_refill(self, request, pk=None):
        """Doctor approves a refill request"""
        prescription = {'id': pk}
        
        return Response({
            'status': 'refill_approved',
            'prescription_id': pk,
            'approved_by': request.user.email,
            'approved_at': datetime.now().isoformat()
        })
    
    @action(detail=True, methods=['post'])
    def deny_refill(self, request, pk=None):
        """Doctor denies a refill request"""
        reason = request.data.get('reason', '')
        
        return Response({
            'status': 'refill_denied',
            'prescription_id': pk,
            'reason': reason,
            'denied_by': request.user.email,
            'denied_at': datetime.now().isoformat()
        })
    
    @action(detail=False, methods=['post'])
    def check_interactions(self, request):
        """Check drug interactions"""
        medications = request.data.get('medications', [])
        
        interactions = []
        for i, med1 in enumerate(medications):
            for med2 in medications[i+1:]:
                interactions.append({
                    'drug_1': med1,
                    'drug_2': med2,
                    'severity': 'moderate',
                    'description': 'Potential interaction detected',
                    'recommendation': 'Consult doctor'
                })
        
        return Response({
            'medications_checked': len(medications),
            'interactions_found': len(interactions),
            'interactions': interactions
        })
    
    @action(detail=True, methods=['get'])
    def export_pdf(self, request, pk=None):
        """Export prescription as PDF"""
        return Response({
            'status': 'pdf_generated',
            'download_url': f'https://storage.example.com/prescriptions/{pk}.pdf',
            'filename': f'prescription_{pk}.pdf'
        })
    
    @action(detail=True, methods=['get'])
    def export_hl7(self, request, pk=None):
        """Export prescription in HL7 format"""
        hl7_data = f"""MSH|^~\\\\&|TELEMED|CLINIC|PHARMACY|SYSTEM|{datetime.now().isoformat()}||ORU^R01|{pk}|P|2.5
RXO|{pk}|ASPIRIN|500MG|PO|BID|||||||||||||||||||||||||
"""
        return Response({
            'status': 'hl7_generated',
            'format': 'HL7v2.5',
            'data': hl7_data
        })
    
    @action(detail=True, methods=['get'])
    def get_history(self, request, pk=None):
        """Get prescription history and modifications"""
        history = [
            {
                'id': 1,
                'action': 'created',
                'action_by': 'Dr. Smith',
                'timestamp': datetime.now().isoformat(),
                'notes': 'Initial prescription'
            },
            {
                'id': 2,
                'action': 'filled',
                'action_by': 'Pharmacy System',
                'timestamp': datetime.now().isoformat(),
                'notes': 'Filled at Local Pharmacy'
            }
        ]
        
        return Response({
            'prescription_id': pk,
            'total_events': len(history),
            'history': history
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get prescription statistics for doctor"""
        return Response({
            'total_prescribed': 145,
            'active_prescriptions': 42,
            'pending_refills': 8,
            'most_prescribed_medication': 'Aspirin',
            'recent_prescriptions': 12,
            'patient_compliance': 0.89
        })
