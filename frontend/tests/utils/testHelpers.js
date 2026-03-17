/**
 * Test Utilities and Fixtures
 */

import { vi } from 'vitest'

// Mock factory functions for test data
export const createMockUser = (overrides = {}) => ({
  id: 1,
  email: 'user@example.com',
  full_name: 'Test User',
  role: 'patient',
  avatar: null,
  created_at: '2026-01-01T00:00:00',
  updated_at: '2026-01-01T00:00:00',
  ...overrides
})

export const createMockDoctor = (overrides = {}) => ({
  id: 1,
  user: createMockUser({
    full_name: 'Dr. Smith',
    role: 'doctor'
  }),
  specialization: 'Cardiology',
  experience_years: 10,
  license_number: 'LIC-12345',
  consultation_fee: 5000,
  rating: 4.8,
  reviews_count: 145,
  is_available: true,
  ...overrides
})

export const createMockPatient = (overrides = {}) => ({
  id: 1,
  user: createMockUser({
    role: 'patient'
  }),
  date_of_birth: '1990-01-01',
  gender: 'M',
  blood_type: 'O+',
  allergies: ['Penicillin'],
  medical_history: [],
  ...overrides
})

export const createMockAppointment = (overrides = {}) => ({
  id: 1,
  doctor: createMockDoctor(),
  patient: createMockPatient(),
  scheduled_at: '2026-03-25T10:00:00',
  duration_minutes: 30,
  status: 'confirmed',
  reason: 'Regular checkup',
  notes: '',
  consultation_type: 'video',
  amount: 5000,
  payment_status: 'completed',
  created_at: '2026-03-20T10:00:00',
  updated_at: '2026-03-20T10:00:00',
  ...overrides
})

export const createMockPrescription = (overrides = {}) => ({
  id: 1,
  doctor: createMockDoctor(),
  patient: createMockPatient(),
  medicine_name: 'Aspirin',
  dosage: '500mg',
  frequency: 'twice daily',
  duration_days: 7,
  instructions: 'Take with water after meals',
  warnings: [],
  refill_count: 0,
  max_refills: 3,
  status: 'active',
  created_at: '2026-03-20T10:00:00',
  expires_at: '2026-06-20T10:00:00',
  ...overrides
})

export const createMockVideoConsultation = (overrides = {}) => ({
  id: 1,
  appointment: createMockAppointment(),
  session_token: 'jitsi-token-12345',
  room_name: 'consultation-room-1',
  started_at: '2026-03-25T10:00:00',
  ended_at: null,
  duration_minutes: 0,
  recording_url: null,
  is_recording: false,
  status: 'active',
  notes: '',
  ...overrides
})

export const createMockAuthState = (overrides = {}) => ({
  user: createMockUser(),
  token: 'jwt-token-abc123',
  refreshToken: 'refresh-token-xyz789',
  isLoading: false,
  error: null,
  isAuthenticated: true,
  ...overrides
})

// Mock API responses
export const mockApiResponses = {
  success: (data) => Promise.resolve({ data, status: 200 }),
  created: (data) => Promise.resolve({ data, status: 201 }),
  noContent: () => Promise.resolve({ status: 204 }),
  badRequest: (message) =>
    Promise.reject({
      response: {
        status: 400,
        data: { error: message }
      }
    }),
  unauthorized: () =>
    Promise.reject({
      response: { status: 401, data: { error: 'Unauthorized' } }
    }),
  forbidden: () =>
    Promise.reject({
      response: { status: 403, data: { error: 'Forbidden' } }
    }),
  notFound: () =>
    Promise.reject({
      response: { status: 404, data: { error: 'Not found' } }
    }),
  serverError: () =>
    Promise.reject({
      response: {
        status: 500,
        data: { error: 'Internal server error' }
      }
    }),
  networkError: () =>
    Promise.reject(new Error('Network error'))
}

// Mock localStorage
export const mockLocalStorage = () => {
  const store = {}
  return {
    getItem: vi.fn((key) => store[key] || null),
    setItem: vi.fn((key, value) => {
      store[key] = value.toString()
    }),
    removeItem: vi.fn((key) => {
      delete store[key]
    }),
    clear: vi.fn(() => {
      Object.keys(store).forEach((key) => delete store[key])
    })
  }
}

// Mock window.location
export const mockWindowLocation = () => {
  const location = {
    href: '',
    pathname: '/',
    search: '',
    hash: '',
    replace: vi.fn(),
  }
  return location
}

// Mock router
export const createMockRouter = (overrides = {}) => ({
  push: vi.fn(),
  replace: vi.fn(),
  go: vi.fn(),
  back: vi.fn(),
  forward: vi.fn(),
  currentRoute: {
    value: {
      name: 'home',
      path: '/',
      params: {},
      query: {},
      ...overrides.currentRoute
    }
  },
  ...overrides
})

// Mock Pinia store
export const createMockAuthStore = (overrides = {}) => ({
  user: null,
  token: null,
  isLoading: false,
  error: null,
  isAuthenticated: false,
  isDoctor: false,
  isPatient: false,
  login: vi.fn(),
  register: vi.fn(),
  logout: vi.fn(),
  fetchUser: vi.fn(),
  updateProfile: vi.fn(),
  changePassword: vi.fn(),
  ...overrides
})

// Test fixtures
export const testFixtures = {
  users: {
    patient: createMockPatient(),
    doctor: createMockDoctor(),
  },
  appointments: {
    pending: createMockAppointment({ status: 'pending' }),
    confirmed: createMockAppointment({ status: 'confirmed' }),
    cancelled: createMockAppointment({ status: 'cancelled' }),
    completed: createMockAppointment({ status: 'completed' }),
  },
  prescriptions: {
    active: createMockPrescription({ status: 'active' }),
    expired: createMockPrescription({
      status: 'expired',
      expires_at: '2026-01-01T00:00:00'
    }),
    refill_requested: createMockPrescription({ status: 'refill_requested' }),
  },
  consultations: {
    active: createMockVideoConsultation({ status: 'active' }),
    completed: createMockVideoConsultation({
      status: 'completed',
      ended_at: '2026-03-25T10:30:00'
    }),
  }
}

// Helper to create array of mock items
export const createMockArray = (factory, count = 3, overridesFn) => {
  return Array.from({ length: count }, (_, index) =>
    factory({
      id: index + 1,
      ...(overridesFn ? overridesFn(index) : {})
    })
  )
}

// Helper to verify mock calls with better error messages
export const expectMockToBeCalledWith = (mockFn, expectedArgs) => {
  const calls = mockFn.mock.calls
  const found = calls.some((call) =>
    JSON.stringify(call) === JSON.stringify(expectedArgs)
  )
  if (!found) {
    throw new Error(
      `Expected mock to be called with ${JSON.stringify(expectedArgs)}, ` +
      `but it was called with: ${calls.map(c => JSON.stringify(c)).join(', ')}`
    )
  }
}

// Helper for async test setup
export const waitFor = (callback, timeout = 1000) =>
  new Promise((resolve, reject) => {
    const start = Date.now()
    const interval = setInterval(() => {
      try {
        callback()
        clearInterval(interval)
        resolve()
      } catch (error) {
        if (Date.now() - start > timeout) {
          clearInterval(interval)
          reject(error)
        }
      }
    }, 50)
  })

// Helper to mock API endpoints
export const mockApiEndpoint = (method, url, response) => {
  const mockFn = vi.fn()
  mockFn.mockImplementation((requestUrl) => {
    if (requestUrl.includes(url)) {
      return mockApiResponses.success(response)
    }
    return mockApiResponses.notFound()
  })
  return mockFn
}
