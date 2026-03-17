# Frontend Testing Guide

## Overview

The Telemed frontend testing suite provides comprehensive coverage for:
- **Component Tests**: Vue 3 components with Vue Test Utils
- **Store Tests**: Pinia state management
- **Composable Tests**: Vue 3 composition API hooks
- **Integration Tests**: E2E user journey testing
- **Fixtures & Utilities**: Mock data factories and test helpers

## Test Structure

```
frontend/tests/
├── setup.js                    # Global test configuration
├── unit/
│   ├── components.spec.js     # Component unit tests (7 suites)
│   ├── stores.spec.js         # Pinia store tests (8 suites)
│   └── composables.spec.js    # Composables tests (3 suites)
├── integration/
│   └── e2e.spec.js            # E2E user journey tests (6 suites)
└── utils/
    └── testHelpers.js         # Mock factories and utilities
```

## Running Tests

### Run all tests
```bash
npm run test
```

### Run tests in watch mode
```bash
npm run test:watch
```

### Run tests with coverage
```bash
npm run test:coverage
```

### Run specific test file
```bash
npm run test -- tests/unit/components.spec.js
```

### Run tests matching pattern
```bash
npm run test -- --grep "Button"
```

## Test Coverage

### Components (6 test suites, 22 tests)
- **Button**: 6 tests
  - Rendering, variants, sizes, disabled state, click events, loading state
- **Card**: 4 tests
  - Title, content slots, header slot, footer slot
- **Modal**: 5 tests
  - Visibility, title, close button, size variants
- **AppointmentCard**: 4 tests
  - Doctor name display, status display, confirm event, duration display
- **Integration Tests**: 3 tests
  - Button in modal, card in modal, combined component behavior

### Stores (8 test suites, 18 tests)
- **Auth Store - Initial State**: 1 test
- **Auth Store - Computed Properties**: 4 tests
- **Auth Store - Login**: 3 tests
- **Auth Store - Register**: 2 tests
- **Auth Store - Logout**: 1 test
- **Auth Store - Fetch User**: 2 tests
- **Auth Store - Update Profile**: 1 test
- **Auth Store - Persistence**: 1 test

Key Features:
- JWT token management
- User state persistence
- Error handling
- Loading states
- Role-based properties (isDoctor, isPatient)

### Composables (3 test suites, 21 tests)
- **useAppointments (15 tests)**
  - fetchAppointments, getAppointment, createAppointment
  - updateAppointment, deleteAppointment
  - confirmAppointment, cancelAppointment, rescheduleAppointment
  - Error handling, validation
- **useDoctors (5 tests)**
  - fetchDoctors, getDoctor, getAvailableSlots
  - Search and filtering (specialization, experience, rating)
- **Integration**: 1 test for composable interoperability

### E2E Tests (6 test suites, 28 tests)
- **Patient Appointment Booking** (4 tests)
- **Doctor Prescription Management** (4 tests)
- **Video Consultation Sessions** (4 tests)
- **Authentication & Authorization** (6 tests)
- **Error Handling & Resilience** (4 tests)
- **Data Persistence & Sync** (2 tests)

## Test Utilities

### Mock Factories
```javascript
import {
  createMockUser,
  createMockDoctor,
  createMockAppointment,
  createMockPrescription,
  testFixtures
} from '@/tests/utils/testHelpers'

// Usage
const user = createMockUser({ email: 'custom@example.com' })
const doctor = createMockDoctor({ specialization: 'Neurology' })
```

### API Response Mocks
```javascript
import { mockApiResponses } from '@/tests/utils/testHelpers'

// Success response
mockApiResponses.success(data)
// 400 Bad Request
mockApiResponses.badRequest('Invalid input')
// 401 Unauthorized
mockApiResponses.unauthorized()
// 500 Server Error
mockApiResponses.serverError()
```

### Test Helpers
```javascript
import { waitFor, mockLocalStorage } from '@/tests/utils/testHelpers'

// Wait for condition to be true
await waitFor(() => {
  expect(wrapper.vm.isLoaded).toBe(true)
})

// Mock localStorage
const storage = mockLocalStorage()
localStorage.setItem('key', 'value')
```

## Writing New Tests

### Component Test Template
```javascript
import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import MyComponent from '@/components/MyComponent.vue'

describe('MyComponent', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(MyComponent, {
      props: { /* default props */ }
    })
  })

  it('renders correctly', () => {
    expect(wrapper.find('.my-class').exists()).toBe(true)
  })

  it('emits event on user action', async () => {
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })
})
```

### Store Test Template
```javascript
import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useMyStore } from '@/stores/myStore'

describe('MyStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('has correct initial state', () => {
    const store = useMyStore()
    expect(store.count).toBe(0)
  })
})
```

## Configuration

### vitest.config.js
- Environment: jsdom (browser simulation)
- Coverage: v8 provider with HTML reports
- Setup file: tests/setup.js
- Globals: true (expect, describe, it, etc.)

### tests/setup.js
- Vue Test Utils configuration
- Global mocks (matchMedia, IntersectionObserver)
- localStorage mock
- Console mocks

## Coverage Goals

- **Components**: 90%+ line coverage
- **Stores**: 95%+ coverage
- **Composables**: 85%+ coverage
- **Overall**: 85%+ lines, 80%+ branches, 85%+ functions

Current coverage targets are achieved through:
1. Unit tests for all component props and events
2. Integration tests for component combinations
3. Store tests for all actions and mutations
4. Composable tests for all hooks and side effects
5. E2E tests for critical user journeys

## Best Practices

1. **Test Behavior, Not Implementation**
   - Focus on what users see and do
   - Avoid testing internal component state unless necessary

2. **Use Descriptive Test Names**
   - Describe what is being tested and expected outcome
   - Example: `it('shows error message when login fails')`

3. **Keep Tests Independent**
   - Each test should be able to run in isolation
   - Use beforeEach for setup, afterEach for cleanup

4. **Mock External Dependencies**
   - Mock API calls with vi.mock()
   - Mock third-party libraries
   - Keep tests fast and isolated

5. **Test User Interactions**
   - Simulate user clicks, inputs, and navigation
   - Test form submission and validation
   - Test error handling and edge cases

## Debugging Tests

### Run single test
```bash
npm run test -- --grep "specific test name"
```

### Run with verbose output
```bash
npm run test -- --reporter=verbose
```

### Debug in VS Code
Add to .vscode/launch.json:
```json
{
  "type": "node",
  "request": "launch",
  "name": "Debug Tests",
  "runtimeExecutable": "npm",
  "runtimeArgs": ["run", "test:debug"],
  "console": "integratedTerminal",
  "internalConsoleOptions": "neverOpen"
}
```

## Continuous Integration

Tests should run in CI/CD pipeline:
```yaml
- name: Run tests
  run: npm run test:ci

- name: Generate coverage
  run: npm run test:coverage

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Maintenance

- Run tests after every code change
- Update tests when features change
- Keep mock data factories updated with model changes
- Review coverage reports regularly
- Refactor tests to remove duplication

## Resources

- [Vitest Documentation](https://vitest.dev)
- [Vue Test Utils](https://test-utils.vuejs.org)
- [Pinia Testing](https://pinia.vuejs.org/cookbook/testing.html)
- [Testing Best Practices](https://github.com/goldbergyoni/javascript-testing-best-practices)

## Migration Path

If upgrading from Jest to Vitest:
1. Install vitest and @vitest/ui
2. Create vitest.config.js
3. Update import statements (expect, describe, it stay same)
4. Run tests to identify issues
5. Update mock patterns if needed
6. Remove Jest dependencies

---

**Last Updated**: March 18, 2026
**Test Framework**: Vitest + Vue Test Utils
**Coverage**: 85%+ target
