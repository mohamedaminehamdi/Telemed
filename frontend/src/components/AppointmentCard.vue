<template>
  <div class="appointment-card">
    <div class="card-header">
      <h3>{{ appointment.doctor.user.full_name }}</h3>
      <span :class="['status-badge', `status-${appointment.status}`]">
        {{ appointment.status }}
      </span>
    </div>
    
    <div class="card-body">
      <div class="appointment-info">
        <div class="info-group">
          <label>Specialization</label>
          <p>{{ appointment.doctor.specialization }}</p>
        </div>
        
        <div class="info-group">
          <label>Date & Time</label>
          <p>{{ formatDateTime(appointment.scheduled_at) }}</p>
        </div>
        
        <div class="info-group">
          <label>Duration</label>
          <p>{{ appointment.duration_minutes }} minutes</p>
        </div>
        
        <div class="info-group">
          <label>Reason</label>
          <p>{{ appointment.reason }}</p>
        </div>
      </div>
    </div>
    
    <div class="card-footer">
      <button 
        v-if="appointment.status === 'pending'"
        @click="handleConfirm" 
        class="btn btn-primary"
      >
        Confirm
      </button>
      
      <button 
        v-if="appointment.status === 'confirmed'"
        @click="handleReschedule" 
        class="btn btn-secondary"
      >
        Reschedule
      </button>
      
      <button 
        v-if="['pending', 'confirmed'].includes(appointment.status)"
        @click="handleCancel" 
        class="btn btn-danger"
      >
        Cancel
      </button>
      
      <button 
        v-if="appointment.status === 'confirmed'"
        @click="handleJoinConsultation" 
        class="btn btn-success"
      >
        Join Consultation
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { formatDateTime } from '@/utils/dateFormatter'

const props = defineProps({
  appointment: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['confirm', 'cancel', 'reschedule', 'join-consultation'])

const handleConfirm = async () => {
  if (confirm('Confirm this appointment?')) {
    emit('confirm', props.appointment.id)
  }
}

const handleCancel = async () => {
  if (confirm('Cancel this appointment?')) {
    emit('cancel', props.appointment.id)
  }
}

const handleReschedule = () => {
  emit('reschedule', props.appointment.id)
}

const handleJoinConsultation = () => {
  emit('join-consultation', props.appointment.id)
}
</script>

<style scoped>
.appointment-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.appointment-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  text-transform: uppercase;
  font-weight: 500;
}

.status-pending {
  background: rgba(255, 193, 7, 0.3);
  color: #f57f17;
}

.status-confirmed {
  background: rgba(76, 175, 80, 0.3);
  color: #388e3c;
}

.status-completed {
  background: rgba(33, 150, 243, 0.3);
  color: #1565c0;
}

.status-cancelled {
  background: rgba(244, 67, 54, 0.3);
  color: #c62828;
}

.card-body {
  padding: 20px;
}

.appointment-info {
  margin-bottom: 16px;
}

.info-group {
  margin-bottom: 12px;
}

.info-group label {
  display: block;
  font-size: 12px;
  text-transform: uppercase;
  color: #999;
  font-weight: 600;
  margin-bottom: 4px;
}

.info-group p {
  margin: 0;
  font-size: 14px;
  color: #333;
}

.card-footer {
  padding: 16px;
  background: #f5f5f5;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #5568d3;
}

.btn-secondary {
  background: #42a5f5;
  color: white;
}

.btn-secondary:hover {
  background: #1e88e5;
}

.btn-danger {
  background: #ef5350;
  color: white;
}

.btn-danger:hover {
  background: #e53935;
}

.btn-success {
  background: #66bb6a;
  color: white;
}

.btn-success:hover {
  background: #43a047;
}
</style>
