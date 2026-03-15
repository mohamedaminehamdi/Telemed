# Backend Tests - Appointments API

from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from datetime import datetime, timedelta


class AppointmentAPITestCase(APITestCase):
    """Test cases for Appointment API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test users
        self.doctor_user = User.objects.create_user(
            username='doctor@test.com',
            email='doctor@test.com',
            password='testpass123'
        )
        
        self.patient_user = User.objects.create_user(
            username='patient@test.com',
            email='patient@test.com',
            password='testpass123'
        )
        
        self.admin_user = User.objects.create_superuser(
            username='admin@test.com',
            email='admin@test.com',
            password='admin123'
        )
    
    def test_appointment_list_requires_authentication(self):
        """Test that appointment list requires authentication"""
        response = self.client.get('/api/v1/appointments/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authenticated_user_can_list_appointments(self):
        """Test that authenticated users can list appointments"""
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.get('/api/v1/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_appointment(self):
        """Test creating an appointment"""
        self.client.force_authenticate(user=self.patient_user)
        
        appointment_data = {
            'doctor_id': 1,
            'scheduled_at': (datetime.now() + timedelta(days=7)).isoformat(),
            'reason': 'Regular checkup',
            'duration_minutes': 30
        }
        
        response = self.client.post('/api/v1/appointments/', appointment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['reason'], 'Regular checkup')
    
    def test_confirm_appointment(self):
        """Test confirming an appointment"""
        self.client.force_authenticate(user=self.doctor_user)
        response = self.client.post('/api/v1/appointments/1/confirm/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'confirmed')
    
    def test_cancel_appointment(self):
        """Test canceling an appointment"""
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.post('/api/v1/appointments/1/cancel/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_reschedule_appointment(self):
        """Test rescheduling an appointment"""
        self.client.force_authenticate(user=self.patient_user)
        
        new_date = (datetime.now() + timedelta(days=14)).isoformat()
        response = self.client.post('/api/v1/appointments/1/reschedule/', {
            'scheduled_at': new_date
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthenticationTestCase(APITestCase):
    """Test cases for authentication endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test@test.com',
            email='test@test.com',
            password='testpass123'
        )
    
    def test_user_registration(self):
        """Test user registration"""
        data = {
            'email': 'newuser@test.com',
            'username': 'newuser',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }
        
        response = self.client.post('/api/v1/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
    
    def test_password_change(self):
        """Test password change"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'old_password': 'testpass123',
            'new_password': 'newpass123!'
        }
        
        response = self.client.post('/api/v1/auth/change_password/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_current_user(self):
        """Test getting current user info"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/auth/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@test.com')


class PermissionTestCase(APITestCase):
    """Test cases for permission checks"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.doctor = User.objects.create_user(
            username='doctor@test.com',
            email='doctor@test.com',
            password='testpass123'
        )
        self.patient = User.objects.create_user(
            username='patient@test.com',
            email='patient@test.com',
            password='testpass123'
        )
    
    def test_doctor_can_create_prescription(self):
        """Test that doctors can create prescriptions"""
        self.client.force_authenticate(user=self.doctor)
        
        data = {
            'appointment_id': 1,
            'medication_name': 'Aspirin',
            'dosage': '500mg',
            'frequency': 'twice daily',
            'duration_days': 7
        }
        
        response = self.client.post('/api/v1/prescriptions/', data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
    
    def test_patient_cannot_create_prescription(self):
        """Test that patients cannot create prescriptions"""
        self.client.force_authenticate(user=self.patient)
        
        data = {
            'appointment_id': 1,
            'medication_name': 'Aspirin',
            'dosage': '500mg',
            'frequency': 'twice daily',
            'duration_days': 7
        }
        
        response = self.client.post('/api/v1/prescriptions/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
