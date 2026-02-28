/**
 * Pinia Store for User Authentication
 * Manages user login, logout, token storage, and user profile
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('auth_token') || null)
  const isLoading = ref(false)
  const error = ref(null)

  // Computed
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isDoctor = computed(() => user.value?.role === 'doctor')
  const isPatient = computed(() => user.value?.role === 'patient')

  // Methods
  const login = async (email, password) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await axios.post('/auth/login/', { email, password })
      token.value = response.data.token
      user.value = response.data.user
      localStorage.setItem('auth_token', token.value)
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Login failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const register = async (userData) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await axios.post('/auth/register/', userData)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Registration failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('auth_token')
    delete axios.defaults.headers.common['Authorization']
  }

  const fetchUser = async () => {
    try {
      const response = await axios.get('/auth/user/')
      user.value = response.data
      return response.data
    } catch (err) {
      logout()
      throw err
    }
  }

  const updateProfile = async (userData) => {
    try {
      const response = await axios.patch('/auth/profile/', userData)
      user.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Update failed'
      throw err
    }
  }

  return {
    // State
    user,
    token,
    isLoading,
    error,
    // Computed
    isAuthenticated,
    isDoctor,
    isPatient,
    // Methods
    login,
    register,
    logout,
    fetchUser,
    updateProfile
  }
})
