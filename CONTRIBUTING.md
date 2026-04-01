# Contributing to Telemed

Thank you for your interest in contributing to the Telemed telemedicine platform! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Constructive feedback only
- Help others succeed
- Report harassment or abuse

## Getting Started

### Prerequisites
- Git knowledge
- Python 3.11+ (for backend)
- Node.js 18+ (for frontend)
- Docker (optional but recommended)
- Familiarity with Django, Vue.js

### Fork & Clone
```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/yourusername/telemed.git
cd telemed

# Add upstream remote
git remote add upstream https://github.com/mohamedaminehamdi/telemed.git
```

### Setup Development Environment

#### Using Docker (Recommended)
```bash
cp .env.example .env
docker-compose up -d
docker-compose exec backend python manage.py migrate
```

#### Without Docker
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate

# Frontend  
cd ../frontend
npm install
```

## Development Workflow

### 1. Create Feature Branch
```bash
# Update main
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
# or for bug fixes
git checkout -b fix/bug-description
# or for docs
git checkout -b docs/documentation-update
```

### 2. Make Changes

#### Backend Changes
- Follow Django style guide (PEP 8)
- Write tests for new functionality
- Update API documentation if endpoints changed
- Add docstrings to functions

```python
# Example: Well-documented backend function
def get_doctor_availability(doctor_id: int, date: str) -> List[Dict]:
    """
    Get available appointment slots for a doctor on a specific date.
    
    Args:
        doctor_id: The ID of the doctor
        date: Date in YYYY-MM-DD format
        
    Returns:
        List of available time slots with details
        
    Raises:
        Doctor.DoesNotExist: If doctor not found
        ValueError: If date format invalid
    """
    # Implementation...
    pass
```

#### Frontend Changes
- Follow Vue 3 composition API patterns
- Write unit tests for components
- Update component documentation
- Keep components under 300 lines

```vue
<!-- Example: Well-structured Vue component -->
<template>
  <div class="appointment-card">
    <header class="card-header">
      <h3>{{ appointment.doctor.user.full_name }}</h3>
    </header>
    <main class="card-body">
      <!-- Content -->
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  appointment: {
    type: Object,
    required: true,
    validator: (obj) => obj.id && obj.doctor
  }
})

const formattedDate = computed(() => {
  return new Date(props.appointment.scheduled_at).toLocaleDateString()
})
</script>

<style scoped>
.appointment-card {
  /* Styles... */
}
</style>
```

### 3. Write Tests

#### Backend Tests
```python
# tests/test_appointments.py
from rest_framework.test import APITestCase
from rest_framework import status

class AppointmentAPITestCase(APITestCase):
    def setUp(self):
        self.patient = User.objects.create_user(
            email='patient@test.com',
            password='testpass123'
        )
        
    def test_list_appointments(self):
        """Test listing appointments for authenticated user"""
        self.client.force_authenticate(user=self.patient)
        response = self.client.get('/api/v1/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

#### Frontend Tests
```javascript
// tests/unit/AppointmentCard.spec.js
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import AppointmentCard from '@/components/AppointmentCard.vue'

describe('AppointmentCard', () => {
  const mockAppointment = {
    id: 1,
    doctor: { user: { full_name: 'Dr. Smith' } },
    scheduled_at: '2026-03-25T10:00:00',
    status: 'confirmed'
  }

  it('displays doctor name', () => {
    const wrapper = mount(AppointmentCard, {
      props: { appointment: mockAppointment }
    })
    expect(wrapper.text()).toContain('Dr. Smith')
  })
})
```

### 4. Run Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd ../frontend
npm run test

# Both with coverage
pytest --cov=apps
npm run test:coverage
```

### 5. Code Quality

#### Linting
```bash
# Backend
pylint backend
flake8 backend
black backend

# Frontend
npm run lint
npm run lint:fix
```

#### Type Checking
```bash
# Backend
mypy backend

# Frontend
npm run type-check
```

### 6. Commit Changes

Write clear, descriptive commit messages:

```bash
# Good commit message
git commit -m "feat: Add video consultation timer display

- Display conversation duration in MM:SS format
- Update every second during active consultation
- Add formatDuration utility function
- Add tests for duration formatting

Closes #123"

# Avoid
git commit -m "fixed stuff"
git commit -m "wip"
```

Commit message format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

### 7. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 8. Create Pull Request

- Go to GitHub and create pull request
- Reference related issues: `Closes #123`
- Describe changes and rationale
- Include screenshots for UI changes
- Ensure CI/CD checks pass

### PR Checklist
- [ ] Tests added/updated
- [ ] Docstrings added
- [ ] No console errors/warnings
- [ ] Code follows style guide
- [ ] Updated relevant documentation
- [ ] Related issues referenced

## Code Style Guide

### Backend (Python/Django)

```python
# Imports
from typing import List, Dict
from datetime import datetime

# Modules
import json
from django.db import models
from rest_framework import serializers

# Constants
DEFAULT_PAGE_SIZE = 20
VALID_STATUSES = ['pending', 'confirmed', 'cancelled']

# Classes - CamelCase
class AppointmentViewSet(viewsets.ModelViewSet):
    pass

# Functions - snake_case
def get_doctors_by_specialization(specialization: str) -> List:
    pass

# Variables - snake_case
doctor_list = []
patient_count = 0

# Constants - UPPER_SNAKE_CASE
MAX_CONSULTATION_DURATION = 3600
```

### Frontend (Vue/JavaScript)

```javascript
// Imports organized
import { ref, computed } from 'vue'
import Button from '@/components/Button.vue'
import { useAppointments } from '@/composables/useAppointments'

// Component props - explicit, with validators
const props = defineProps({
  appointment: {
    type: Object,
    required: true
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

// Constants - UPPER_SNAKE_CASE
const MAX_TITLE_LENGTH = 100

// Reactive state
const count = ref(0)
const appointments = ref([])

// Computed properties
const displayTitle = computed(() => {
  return appointments.value.length > 0
})

// Methods - camelCase
const handleSubmit = async () => {
  // Implementation
}
```

## Documentation

### Backend API Documentation
```python
"""
Module: appointments.views

Handles all appointment-related API endpoints including scheduling,
confirmation, cancellation, and rescheduling operations.
"""

class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing appointments.
    
    Supports full CRUD operations and custom actions for
    confirming, cancelling, and rescheduling appointments.
    """
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """
        Confirm a pending appointment.
        
        Args:
            request: HTTP request object
            pk: Appointment ID
            
        Returns:
            Updated appointment data
            
        Raises:
            ValidationError: If appointment is not pending
        """
        pass
```

### Frontend Component Documentation
```vue
<!-- 
AppointmentCard.vue

Displays appointment information in card format with action buttons.

Props:
  - appointment (Object, required): Appointment data
    - id: Appointment ID
    - doctor: Doctor information object
    - scheduled_at: ISO datetime string
    - status: One of 'pending', 'confirmed', 'cancelled'
    - reason: Reason for appointment

Emits:
  - confirm: Fired when confirm button clicked
  - cancel: Fired when cancel button clicked  
  - reschedule: Fired when reschedule initiated

Slots:
  - default: Additional content below appointment info
  - actions: Custom action buttons

Example:
  <AppointmentCard 
    :appointment="appointment"
    @confirm="handleConfirm"
    @cancel="handleCancel"
  />
-->
<template>
  <!-- Component JSX -->
</template>
```

## Reporting Issues

### Bug Report Template
```
**Describe the bug**
Clear description of the problem

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What should happen instead

**Screenshots**
If applicable, add screenshots

**Environment**
- OS: Ubuntu 22.04
- Browser: Chrome 120
- Python: 3.11
- Node: 18.0
```

### Feature Request Template
```
**Is your feature request related to a problem?**
Description of the problem

**Describe the solution you'd like**
Clear description of desired feature

**Describe alternatives you've considered**
Alternative solutions

**Additional context**
Any other relevant information
```

## Review Process

### What Reviewers Look For
- [ ] Code quality and style
- [ ] Test coverage
- [ ] Documentation completeness
- [ ] Breaking changes
- [ ] Performance impact
- [ ] Security implications

### Addressing Review Comments
- Don't take criticism personally
- Ask for clarification if needed
- Make requested changes promptly
- Re-request review after changes

## Release Process

### Versioning
Follow [Semantic Versioning](https://semver.org/):
- MAJOR.MINOR.PATCH (e.g., 1.0.0)
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Release Checklist
- [ ] All tests passing
- [ ] Coverage at acceptable level
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version bumped
- [ ] Release notes written
- [ ] Tagged in Git
- [ ] Published to registry/GitHub

## Resources

- [Git Workflow](https://guides.github.com/introduction/flow/)
- [Django Coding Standards](https://docs.djangoproject.com/en/stable/internals/contributing/)
- [Vue 3 Style Guide](https://vuejs.org/guide/scaling-up/sfc-spec.html)
- [Testing Best Practices](https://github.com/goldbergyoni/javascript-testing-best-practices)
- [API Design Principles](https://restfulapi.net/)

## Getting Help

- **Issues**: Post in GitHub Issues
- **Discussions**: Start a discussion thread
- **Documentation**: Check existing docs
- **Examples**: Review test files
- **Chat**: Community Discord (if available)

## Recognition

Contributors are recognized in:
- README.md Contributors section
- Release notes
- GitHub insights page
- Project acknowledgments

---

**Thank you for contributing to Telemed! Together we're making healthcare more accessible. 🎉**

**Questions? Create an issue or start a discussion!**
