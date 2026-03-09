<template>
  <div class="prescriptions-container">
    <div class="prescriptions-header">
      <h2>Prescriptions</h2>
      <div class="header-actions">
        <button v-if="isDoctor" @click="showCreateForm = true" class="btn-primary">
          + New Prescription
        </button>
        <button @click="toggleView" class="btn-secondary">
          {{ viewMode === 'list' ? 'Calendar View' : 'List View' }}
        </button>
      </div>
    </div>

    <!-- Create/Edit Prescription Form -->
    <div v-if="showCreateForm" class="modal-overlay">
      <div class="modal-content prescription-form">
        <div class="form-header">
          <h3>{{ editingId ? 'Edit Prescription' : 'Create Prescription' }}</h3>
          <button @click="showCreateForm = false" class="close-btn">✕</button>
        </div>

        <form @submit.prevent="savePrescription">
          <div class="form-group">
            <label>Medication Name</label>
            <input
              v-model="form.medicationName"
              type="text"
              placeholder="e.g., Aspirin"
              required
            />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Dosage</label>
              <input
                v-model="form.dosage"
                type="text"
                placeholder="e.g., 500mg"
                required
              />
            </div>
            <div class="form-group">
              <label>Frequency</label>
              <select v-model="form.frequency">
                <option>Once daily</option>
                <option>Twice daily</option>
                <option>Three times daily</option>
                <option>Four times daily</option>
                <option>As needed</option>
              </select>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Duration (days)</label>
              <input
                v-model.number="form.durationDays"
                type="number"
                min="1"
                required
              />
            </div>
            <div class="form-group">
              <label>Quantity</label>
              <input
                v-model.number="form.quantity"
                type="number"
                min="1"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label>Instructions</label>
            <textarea
              v-model="form.instructions"
              placeholder="e.g., Take with food"
              rows="3"
            ></textarea>
          </div>

          <div class="form-group">
            <label>Warnings</label>
            <textarea
              v-model="form.warnings"
              placeholder="e.g., May cause dizziness"
              rows="2"
            ></textarea>
          </div>

          <div class="form-group checkbox">
            <input
              v-model="form.isControlled"
              type="checkbox"
              id="controlled"
            />
            <label for="controlled">Controlled Substance</label>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-submit">
              {{ editingId ? 'Update' : 'Create' }} Prescription
            </button>
            <button type="button" @click="showCreateForm = false" class="btn-cancel">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Refill Request Dialog -->
    <div v-if="showRefillDialog" class="modal-overlay">
      <div class="modal-content refill-form">
        <h3>Request Prescription Refill</h3>
        
        <div class="form-group">
          <label>Number of Refills</label>
          <select v-model.number="refillCount">
            <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
          </select>
        </div>

        <div class="form-group">
          <label>Reason for Refill (optional)</label>
          <textarea v-model="refillReason" rows="3" placeholder="Add any additional notes..."></textarea>
        </div>

        <div class="form-actions">
          <button @click="submitRefillRequest" class="btn-submit">Request Refill</button>
          <button @click="showRefillDialog = false" class="btn-cancel">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Prescriptions List -->
    <div v-if="viewMode === 'list'" class="prescriptions-list">
      <div v-if="prescriptions.length === 0" class="empty-state">
        <p>No prescriptions yet</p>
      </div>

      <div v-for="prescription in prescriptions" :key="prescription.id" class="prescription-card">
        <div class="card-header">
          <div class="medication-info">
            <h4>{{ prescription.medicationName }}</h4>
            <p class="dosage">{{ prescription.dosage }} · {{ prescription.frequency }}</p>
          </div>
          <span :class="['status-badge', `status-${prescription.status}`]">
            {{ prescription.status }}
          </span>
        </div>

        <div class="card-body">
          <div class="info-grid">
            <div class="info-item">
              <label>Duration</label>
              <p>{{ prescription.durationDays }} days</p>
            </div>
            <div class="info-item">
              <label>Quantity</label>
              <p>{{ prescription.quantity }}</p>
            </div>
            <div class="info-item">
              <label>Refills</label>
              <p>{{ prescription.refillsAllowed }}</p>
            </div>
            <div class="info-item">
              <label>Expires</label>
              <p>{{ formatDate(prescription.expiresAt) }}</p>
            </div>
          </div>

          <div v-if="prescription.instructions" class="instructions">
            <strong>Instructions:</strong>
            <p>{{ prescription.instructions }}</p>
          </div>

          <div v-if="prescription.warnings" class="warnings">
            <strong>⚠️ Warnings:</strong>
            <p>{{ prescription.warnings }}</p>
          </div>
        </div>

        <div class="card-actions">
          <button
            v-if="canRefill(prescription)"
            @click="openRefillDialog(prescription)"
            class="btn-action refill"
          >
            Request Refill
          </button>
          
          <button
            v-if="isDoctor"
            @click="editPrescription(prescription)"
            class="btn-action edit"
          >
            Edit
          </button>

          <button
            @click="exportPdforPrescription(prescription)"
            class="btn-action export"
          >
            Download PDF
          </button>
        </div>
      </div>
    </div>

    <!-- Calendar View -->
    <div v-else class="prescriptions-calendar">
      <!-- Placeholder for calendar view -->
      <div class="calendar-placeholder">
        <p>Calendar view coming soon</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { formatDate } from '@/utils/dateFormatter'

const isDoctor = ref(false)  // Set based on user role
const viewMode = ref('list')
const showCreateForm = ref(false)
const showRefillDialog = ref(false)
const editingId = ref(null)
const selectedPrescription = ref(null)

const form = ref({
  medicationName: '',
  dosage: '',
  frequency: 'Once daily',
  durationDays: 7,
  quantity: 30,
  instructions: '',
  warnings: '',
  isControlled: false
})

const refillCount = ref(1)
const refillReason = ref('')

const prescriptions = ref([
  {
    id: 1,
    medicationName: 'Aspirin',
    dosage: '500mg',
    frequency: 'Twice daily',
    durationDays: 7,
    quantity: 14,
    refillsAllowed: 2,
    instructions: 'Take with food',
    warnings: 'May cause stomach upset',
    status: 'active',
    expiresAt: '2026-04-06'
  },
  {
    id: 2,
    medicationName: 'Ibuprofen',
    dosage: '200mg',
    frequency: 'Three times daily',
    durationDays: 10,
    quantity: 30,
    refillsAllowed: 0,
    instructions: 'Take with meals',
    warnings: 'Do not exceed recommended dose',
    status: 'active',
    expiresAt: '2026-03-16'
  }
])

const toggleView = () => {
  viewMode.value = viewMode.value === 'list' ? 'calendar' : 'list'
}

const savePrescription = async () => {
  // Save prescription logic
  if (!editingId.value) {
    prescriptions.value.push({
      id: Date.now(),
      ...form.value,
      status: 'active',
      expiresAt: new Date(Date.now() + form.value.durationDays * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
    })
  }
  
  resetForm()
  showCreateForm.value = false
}

const resetForm = () => {
  form.value = {
    medicationName: '',
    dosage: '',
    frequency: 'Once daily',
    durationDays: 7,
    quantity: 30,
    instructions: '',
    warnings: '',
    isControlled: false
  }
  editingId.value = null
}

const editPrescription = (prescription) => {
  editingId.value = prescription.id
  form.value = { ...prescription }
  showCreateForm.value = true
}

const canRefill = (prescription) => {
  return prescription.refillsAllowed > 0 && prescription.status === 'active'
}

const openRefillDialog = (prescription) => {
  selectedPrescription.value = prescription
  showRefillDialog.value = true
}

const submitRefillRequest = async () => {
  // Submit refill request
  console.log('Requesting refill:', selectedPrescription.value.id, refillCount.value)
  showRefillDialog.value = false
  selectedPrescription.value = null
  refillCount.value = 1
  refillReason.value = ''
}

const exportPdforPrescription = (prescription) => {
  console.log('Exporting prescription:', prescription.id)
  // Implement PDF export
}
</script>

<style scoped>
.prescriptions-container {
  padding: 20px;
  background: #f5f5f5;
  min-height: 100vh;
}

.prescriptions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  background: white;
  padding: 20px;
  border-radius: 8px;
}

.prescriptions-header h2 {
  margin: 0;
  font-size: 28px;
  color: #333;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn-primary, .btn-secondary {
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: white;
  color: #667eea;
  border: 1px solid #667eea;
}

.btn-secondary:hover {
  background: #f5f5f5;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 32px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.form-header h3 {
  margin: 0;
  font-size: 20px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

/* Form Styles */
.form-group {
  margin-bottom: 16px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 6px;
  font-size: 12px;
  text-transform: uppercase;
  color: #667eea;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-family: inherit;
  font-size: 14px;
  box-sizing: border-box;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group textarea {
  resize: vertical;
}

.form-group.checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-group.checkbox input {
  width: auto;
  margin: 0;
}

.form-group.checkbox label {
  margin: 0;
  text-transform: none;
  color: #333;
}

.form-actions {
  display: flex;
  gap: 8px;
  margin-top: 24px;
}

.btn-submit {
  flex: 1;
  padding: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-cancel {
  flex: 1;
  padding: 12px;
  background: #f0f0f0;
  color: #333;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
}

.btn-cancel:hover {
  background: #e0e0e0;
}

/* Prescriptions List */
.prescriptions-list {
  display: grid;
  gap: 16px;
}

.empty-state {
  background: white;
  padding: 40px;
  border-radius: 8px;
  text-align: center;
  color: #999;
}

.prescription-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.prescription-card:hover {
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

.medication-info h4 {
  margin: 0;
  font-size: 18px;
}

.dosage {
  margin: 4px 0 0;
  font-size: 13px;
  opacity: 0.9;
}

.status-badge {
  padding: 4px 12px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
}

.status-active {
  background: rgba(76, 175, 80, 0.3);
  color: white;
}

.card-body {
  padding: 20px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.info-item label {
  display: block;
  font-size: 11px;
  text-transform: uppercase;
  color: #999;
  font-weight: 600;
  margin-bottom: 4px;
}

.info-item p {
  margin: 0;
  font-size: 13px;
  color: #333;
  font-weight: 500;
}

.instructions,
.warnings {
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 12px;
  font-size: 13px;
  line-height: 1.5;
}

.instructions {
  background: #f0f7ff;
  border-left: 4px solid #667eea;
}

.warnings {
  background: #fff3e0;
  border-left: 4px solid #ff9800;
}

.instructions strong,
.warnings strong {
  display: block;
  margin-bottom: 6px;
  color: #333;
}

.instructions p,
.warnings p {
  margin: 0;
  color: #555;
}

.card-actions {
  padding: 12px 20px;
  background: #f9f9f9;
  border-top: 1px solid #f0f0f0;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.btn-action {
  padding: 6px 12px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.btn-action:hover {
  border-color: #667eea;
  color: #667eea;
}

.btn-action.refill {
  border-color: #4caf50;
  color: #4caf50;
}

.btn-action.refill:hover {
  background: #f1f8f5;
}

.calendar-placeholder {
  background: white;
  padding: 40px;
  border-radius: 8px;
  text-align: center;
  color: #999;
}

@media (max-width: 768px) {
  .prescriptions-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .info-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .modal-content {
    padding: 20px;
  }
}
</style>
