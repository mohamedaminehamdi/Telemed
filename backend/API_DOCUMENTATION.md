# Telemed Backend API Documentation

## Overview

The Telemed API provides comprehensive endpoints for managing telemedicine operations including:
- Appointments scheduling and management
- Doctor and patient profiles
- Prescriptions
- Video consultations
- User authentication and authorization

## Base URL

```
http://localhost:8000/api/v1/
```

## Authentication

All endpoints require Bearer token authentication:

```
Authorization: Bearer <token>
```

## Endpoints

### Appointments

#### List Appointments
```
GET /api/v1/appointments/
Query Parameters:
  - status: pending, confirmed, cancelled, completed
  - doctor: doctor_id
  - patient: patient_id
  - page: page_number
  - page_size: items_per_page
```

#### Create Appointment
```
POST /api/v1/appointments/
Body:
{
  "doctor_id": 1,
  "scheduled_at": "2026-04-15T10:00:00Z",
  "reason": "Regular checkup",
  "notes": "Optional notes"
}
```

#### Confirm Appointment
```
POST /api/v1/appointments/{id}/confirm/
```

#### Cancel Appointment
```
POST /api/v1/appointments/{id}/cancel/
```

#### Reschedule Appointment
```
POST /api/v1/appointments/{id}/reschedule/
Body:
{
  "scheduled_at": "2026-04-16T14:00:00Z"
}
```

### Doctors

#### List Doctors
```
GET /api/v1/doctors/
Query Parameters:
  - specialization: surgery, cardiology, pediatrics, etc.
  - is_available: true, false
  - search: name search
  - page: pagination
```

#### Doctor Details
```
GET /api/v1/doctors/{id}/
```

#### Available Slots
```
GET /api/v1/doctors/{id}/available_slots/?date=2026-04-15
Response:
{
  "doctor_id": 1,
  "date": "2026-04-15",
  "available_slots": ["09:00", "10:00", "11:00", "14:00", "15:00"]
}
```

### Prescriptions

#### List Prescriptions
```
GET /api/v1/prescriptions/
Query Parameters:
  - appointment: appointment_id
  - page: pagination
```

#### Create Prescription
```
POST /api/v1/prescriptions/
Body:
{
  "appointment_id": 1,
  "medication_name": "Aspirin",
  "dosage": "500mg",
  "frequency": "twice daily",
  "duration_days": 7,
  "instructions": "Take with food"
}
```

### Consultations

#### Start Consultation
```
POST /api/v1/consultations/
Body:
{
  "appointment_id": 1,
  "video_session_id": "session_abc123"
}
```

#### End Consultation
```
POST /api/v1/consultations/{id}/end_session/
```

#### Upload Recording
```
POST /api/v1/consultations/{id}/upload_recording/
Body: FormData
{
  "recording": <file>
}
```

## Pagination

List endpoints use pagination:

```json
{
  "count": 100,
  "next": "http://localhost:8000/api/v1/appointments/?page=2",
  "previous": null,
  "results": [...]
}
```

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 400 Bad Request
```json
{
  "error": "Field name is required."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

## Rate Limiting

API implements rate limiting:
- Anonymous: 100 requests/hour
- Authenticated: 1000 requests/hour

## Versioning

API uses URL versioning: `/api/v1/`

## CORS

CORS is enabled for frontend domains specified in settings.

## Testing

Use the following credentials for testing:

```
Username: doctor@test.com
Password: testpass123

Username: patient@test.com
Password: testpass123
```

## Support

For issues or questions, contact: api-support@telemed.com
