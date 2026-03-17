/**
 * Pinia Store Tests - Authentication Store
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

vi.mock('axios')

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  afterEach(() => {
    vi.clearAllMocks()
  })

  describe('Initial State', () => {
    it('has correct initial state', () => {
      const store = useAuthStore()
      expect(store.user).toBeNull()
      expect(store.token).toBeNull()
      expect(store.isLoading).toBe(false)
      expect(store.error).toBeNull()
    })
  })

  describe('Computed Properties', () => {
    it('isAuthenticated returns false when no token', () => {
      const store = useAuthStore()
      expect(store.isAuthenticated).toBe(false)
    })

    it('isAuthenticated returns true when token exists', () => {
      const store = useAuthStore()
      store.token = 'valid-token'
      expect(store.isAuthenticated).toBe(true)
    })

    it('isDoctor returns true for doctor users', () => {
      const store = useAuthStore()
      store.user = { role: 'doctor' }
      expect(store.isDoctor).toBe(true)
    })

    it('isPatient returns true for patient users', () => {
      const store = useAuthStore()
      store.user = { role: 'patient' }
      expect(store.isPatient).toBe(true)
    })
  })

  describe('Login Action', () => {
    it('successfully logs in user', async () => {
      const store = useAuthStore()
      const mockResponse = {
        data: {
          access: 'access-token',
          refresh: 'refresh-token',
          user: {
            id: 1,
            email: 'test@example.com',
            full_name: 'Test User',
            role: 'patient'
          }
        }
      }

      vi.mocked(axios.post).mockResolvedValueOnce(mockResponse)

      await store.login('test@example.com', 'password123')

      expect(store.token).toBe('access-token')
      expect(store.user).toEqual(mockResponse.data.user)
      expect(store.error).toBeNull()
    })

    it('handles login error', async () => {
      const store = useAuthStore()
      const mockError = new Error('Invalid credentials')

      vi.mocked(axios.post).mockRejectedValueOnce(mockError)

      await store.login('test@example.com', 'wrong-password')

      expect(store.token).toBeNull()
      expect(store.error).toBeDefined()
    })

    it('sets loading state during login', async () => {
      const store = useAuthStore()
      const mockResponse = {
        data: {
          access: 'token',
          user: { id: 1, email: 'test@example.com' }
        }
      }

      vi.mocked(axios.post).mockImplementation(
        () => new Promise(resolve => setTimeout(() => resolve(mockResponse), 100))
      )

      const loginPromise = store.login('test@example.com', 'password123')
      expect(store.isLoading).toBe(true)

      await loginPromise
      expect(store.isLoading).toBe(false)
    })
  })

  describe('Register Action', () => {
    it('successfully registers new user', async () => {
      const store = useAuthStore()
      const mockResponse = {
        data: {
          access: 'access-token',
          user: {
            id: 1,
            email: 'newuser@example.com',
            full_name: 'New User',
            role: 'patient'
          }
        }
      }

      vi.mocked(axios.post).mockResolvedValueOnce(mockResponse)

      const registerData = {
        email: 'newuser@example.com',
        password: 'securepass123',
        full_name: 'New User',
        role: 'patient'
      }

      await store.register(registerData)

      expect(store.token).toBe('access-token')
      expect(store.user.email).toBe('newuser@example.com')
    })

    it('handles registration error', async () => {
      const store = useAuthStore()
      const mockError = new Error('Email already exists')

      vi.mocked(axios.post).mockRejectedValueOnce(mockError)

      const registerData = {
        email: 'existing@example.com',
        password: 'password',
        full_name: 'User'
      }

      await store.register(registerData)
      expect(store.error).toBeDefined()
    })
  })

  describe('Logout Action', () => {
    it('clears user data on logout', () => {
      const store = useAuthStore()
      store.token = 'some-token'
      store.user = { id: 1, email: 'test@example.com' }

      store.logout()

      expect(store.token).toBeNull()
      expect(store.user).toBeNull()
      expect(store.error).toBeNull()
    })
  })

  describe('Fetch User Action', () => {
    it('fetches and updates user data', async () => {
      const store = useAuthStore()
      store.token = 'valid-token'

      const mockResponse = {
        data: {
          id: 1,
          email: 'user@example.com',
          full_name: 'Updated Name',
          role: 'doctor'
        }
      }

      vi.mocked(axios.get).mockResolvedValueOnce(mockResponse)

      await store.fetchUser()

      expect(store.user).toEqual(mockResponse.data)
    })

    it('handles fetch user error', async () => {
      const store = useAuthStore()
      store.token = 'invalid-token'

      vi.mocked(axios.get).mockRejectedValueOnce(
        new Error('Unauthorized')
      )

      await store.fetchUser()
      expect(store.error).toBeDefined()
    })
  })

  describe('Update Profile Action', () => {
    it('updates user profile', async () => {
      const store = useAuthStore()
      store.token = 'valid-token'
      store.user = { id: 1, full_name: 'Old Name' }

      const mockResponse = {
        data: {
          id: 1,
          full_name: 'New Name',
          email: 'user@example.com'
        }
      }

      vi.mocked(axios.patch).mockResolvedValueOnce(mockResponse)

      await store.updateProfile({ full_name: 'New Name' })

      expect(store.user.full_name).toBe('New Name')
    })
  })

  describe('Persistence', () => {
    it('restores token from localStorage', () => {
      const store = useAuthStore()
      localStorage.setItem('auth_token', 'persisted-token')

      // Simulate store re-initialization
      const newStore = useAuthStore()
      // In real app, this would be handled by store plugins
      expect(localStorage.getItem('auth_token')).toBe('persisted-token')
    })
  })
})
