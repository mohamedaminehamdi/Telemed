/**
 * Composable for managing appointments
 * Handles appointment CRUD and custom actions
 */

import { ref, computed } from 'vue'
import axios from '@/services/api'

export const useAppointments = () => {
  const appointments = ref([])
  const loading = ref(false)
  const error = ref(null)
  const currentAppointment = ref(null)

  const fetchAppointments = async (filters = {}) => {
    loading.value = true
    error.value = null
    try {
      const params = new URLSearchParams(filters)
      const response = await axios.get(`/appointments/?${params}`)
      appointments.value = response.data.results || response.data
      return appointments.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const getAppointment = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get(`/appointments/${id}/`)
      currentAppointment.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const createAppointment = async (data) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post('/appointments/', data)
      appointments.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateAppointment = async (id, data) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.patch(`/appointments/${id}/`, data)
      const index = appointments.value.findIndex(a => a.id === id)
      if (index > -1) {
        appointments.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteAppointment = async (id) => {
    loading.value = true
    error.value = null
    try {
      await axios.delete(`/appointments/${id}/`)
      appointments.value = appointments.value.filter(a => a.id !== id)
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const confirmAppointment = async (id) => {
    try {
      const response = await axios.post(`/appointments/${id}/confirm/`)
      const index = appointments.value.findIndex(a => a.id === id)
      if (index > -1) {
        appointments.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const cancelAppointment = async (id) => {
    try {
      await axios.post(`/appointments/${id}/cancel/`)
      const index = appointments.value.findIndex(a => a.id === id)
      if (index > -1) {
        appointments.value[index].status = 'cancelled'
      }
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const rescheduleAppointment = async (id, newDate) => {
    try {
      const response = await axios.post(`/appointments/${id}/reschedule/`, {
        scheduled_at: newDate
      })
      const index = appointments.value.findIndex(a => a.id === id)
      if (index > -1) {
        appointments.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  return {
    // State
    appointments,
    loading,
    error,
    currentAppointment,
    // Methods
    fetchAppointments,
    getAppointment,
    createAppointment,
    updateAppointment,
    deleteAppointment,
    confirmAppointment,
    cancelAppointment,
    rescheduleAppointment
  }
}

/**
 * Composable for managing doctors
 */
export const useDoctors = () => {
  const doctors = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchDoctors = async (filters = {}) => {
    loading.value = true
    error.value = null
    try {
      const params = new URLSearchParams(filters)
      const response = await axios.get(`/doctors/?${params}`)
      doctors.value = response.data.results || response.data
      return doctors.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const getDoctor = async (id) => {
    try {
      const response = await axios.get(`/doctors/${id}/`)
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const getAvailableSlots = async (doctorId, date) => {
    try {
      const response = await axios.get(`/doctors/${doctorId}/available_slots/`, {
        params: { date }
      })
      return response.data.available_slots
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  return {
    doctors,
    loading,
    error,
    fetchDoctors,
    getDoctor,
    getAvailableSlots
  }
}
