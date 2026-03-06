<template>
  <div class="video-consultation">
    <div v-if="!sessionActive" class="consultation-pre">
      <div class="pre-call">
        <div class="camera-preview">
          <video
            ref="previewVideo"
            autoplay
            muted
            playsinline
            class="preview-stream"
          ></video>
          <div class="device-controls">
            <button
              @click="toggleCamera"
              :class="['device-btn', { 'device-off': !cameraOn }]"
            >
              <span class="icon">🎥</span>
              {{ cameraOn ? 'Camera On' : 'Camera Off' }}
            </button>
            <button
              @click="toggleMicrophone"
              :class="['device-btn', { 'device-off': !microphoneOn }]"
            >
              <span class="icon">🎤</span>
              {{ microphoneOn ? 'Mic On' : 'Mic Off' }}
            </button>
          </div>
        </div>

        <div class="pre-call-info">
          <h3>Ready to start consultation?</h3>
          <div class="participant-info">
            <div class="participant">
              <div class="avatar-placeholder">👨‍⚕️</div>
              <p>Dr. {{ doctorName }}</p>
            </div>
            <div class="vs-text">VS</div>
            <div class="participant">
              <div class="avatar-placeholder">👤</div>
              <p>{{ patientName }}</p>
            </div>
          </div>

          <div class="pre-call-actions">
            <button @click="startConsultation" class="btn-start" :disabled="isStarting">
              <span v-if="isStarting">Starting...</span>
              <span v-else>Start Consultation</span>
            </button>
            <button @click="cancelConsultation" class="btn-cancel">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="consultation-active">
      <div class="video-grid">
        <div class="video-container remote">
          <video
            ref="remoteVideo"
            autoplay
            playsinline
            class="video-stream"
          ></video>
          <div class="user-label">Dr. {{ doctorName }}</div>
        </div>
        
        <div class="video-container local">
          <video
            ref="localVideo"
            autoplay
            muted
            playsinline
            class="video-stream"
          ></video>
          <div class="user-label">{{ patientName }} (You)</div>
        </div>
      </div>

      <div class="consultation-controls">
        <div class="duration">{{ formattedDuration }}</div>
        
        <div class="call-actions">
          <button
            @click="toggleCamera"
            :class="['action-btn', { inactive: !cameraOn }]"
            title="Toggle Camera"
          >
            <span v-if="cameraOn">🎥</span>
            <span v-else>📹</span>
          </button>

          <button
            @click="toggleMicrophone"
            :class="['action-btn', { inactive: !microphoneOn }]"
            title="Toggle Microphone"
          >
            <span v-if="microphoneOn">🎤</span>
            <span v-else>🔇</span>
          </button>

          <button
            @click="toggleScreenShare"
            :class="['action-btn', { active: screenSharing }]"
            title="Share Screen"
          >
            🖥️
          </button>

          <button
            @click="showChat = !showChat"
            class="action-btn"
            title="Toggle Chat"
          >
            💬
          </button>

          <button
            @click="toggleRecording"
            :class="['action-btn', { recording: isRecording }]"
            title="Toggle Recording"
          >
            {{ isRecording ? '⏹️' : '⏱️' }}
          </button>

          <button
            @click="endConsultation"
            class="action-btn end-call"
            title="End Call"
          >
            📞
          </button>
        </div>
      </div>

      <!-- Chat Panel -->
      <div v-if="showChat" class="chat-panel">
        <div class="chat-header">
          <h4>Chat</h4>
          <button @click="showChat = false" class="close-btn">✕</button>
        </div>
        <div class="chat-messages">
          <div
            v-for="msg in chatMessages"
            :key="msg.id"
            :class="['message', { own: msg.own }]"
          >
            <p class="message-sender">{{ msg.sender }}</p>
            <p class="message-text">{{ msg.text }}</p>
            <p class="message-time">{{ msg.time }}</p>
          </div>
        </div>
        <div class="chat-input">
          <input
            v-model="chatMessage"
            @keyup.enter="sendMessage"
            type="text"
            placeholder="Type a message..."
          />
          <button @click="sendMessage">Send</button>
        </div>
      </div>
    </div>

    <!-- End Consultation Dialog -->
    <div v-if="showEndDialog" class="modal-overlay">
      <div class="modal-content">
        <h3>End Consultation?</h3>
        <p>Are you sure you want to end this consultation?</p>
        
        <div class="form-group">
          <label>Session Notes (optional)</label>
          <textarea
            v-model="sessionNotes"
            placeholder="Add notes about the consultation..."
            rows="4"
          ></textarea>
        </div>

        <div class="modal-actions">
          <button @click="confirmEndConsultation" class="btn-confirm">
            End Consultation
          </button>
          <button @click="showEndDialog = false" class="btn-cancel">
            Continue
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Video elements
const previewVideo = ref(null)
const localVideo = ref(null)
const remoteVideo = ref(null)

// State
const sessionActive = ref(false)
const isStarting = ref(false)
const cameraOn = ref(true)
const microphoneOn = ref(true)
const screenSharing = ref(false)
const isRecording = ref(false)
const showChat = ref(false)
const showEndDialog = ref(false)

const appointmentId = ref(1)
const doctorName = ref('Smith')
const patientName = ref('Doe')
const sessionStartTime = ref(null)
const duration = ref(0)
const sessionNotes = ref('')
const chatMessage = ref('')
const chatMessages = ref([
  { id: 1, sender: 'Dr. Smith', text: 'Hi, how are you feeling today?', own: false, time: '10:00 AM' },
  { id: 2, sender: 'Patient', text: 'I have been experiencing headaches', own: true, time: '10:01 AM' }
])

const formattedDuration = computed(() => {
  const minutes = Math.floor(duration.value / 60)
  const seconds = duration.value % 60
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
})

// Methods
const toggleCamera = async () => {
  cameraOn.value = !cameraOn.value
  // Implement camera toggle logic
}

const toggleMicrophone = async () => {
  microphoneOn.value = !microphoneOn.value
  // Implement microphone toggle logic
}

const toggleScreenShare = async () => {
  screenSharing.value = !screenSharing.value
  // Implement screen sharing logic
}

const toggleRecording = () => {
  isRecording.value = !isRecording.value
  // Implement recording toggle
}

const startConsultation = async () => {
  isStarting.value = true
  sessionActive.value = true
  sessionStartTime.value = Date.now()
}

const endConsultation = () => {
  showEndDialog.value = true
}

const confirmEndConsultation = async () => {
  // Send session notes and end consultation
  console.log('Ending consultation with notes:', sessionNotes.value)
  sessionActive.value = false
  showEndDialog.value = false
  router.push('/consultations')
}

const cancelConsultation = () => {
  router.back()
}

const sendMessage = () => {
  if (chatMessage.value.trim()) {
    const newMessage = {
      id: chatMessages.value.length + 1,
      sender: 'You',
      text: chatMessage.value,
      own: true,
      time: new Date().toLocaleTimeString()
    }
    chatMessages.value.push(newMessage)
    chatMessage.value = ''
  }
}

// Update duration timer
onMounted(() => {
  const interval = setInterval(() => {
    if (sessionActive.value && sessionStartTime.value) {
      duration.value = Math.floor((Date.now() - sessionStartTime.value) / 1000)
    }
  }, 1000)

  onUnmounted(() => clearInterval(interval))
})
</script>

<style scoped>
.video-consultation {
  width: 100%;
  height: 100vh;
  background: #000;
  display: flex;
  flex-direction: column;
}

/* Pre-call screen */
.consultation-pre {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.pre-call {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  width: 100%;
  max-width: 1000px;
}

.camera-preview {
  position: relative;
  background: #1a1a1a;
  border-radius: 12px;
  overflow: hidden;
}

.preview-stream {
  width: 100%;
  height: 400px;
  object-fit: cover;
}

.device-controls {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 12px;
  z-index: 10;
}

.device-btn {
  padding: 8px 12px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
}

.device-off {
  background: rgba(255, 0, 0, 0.6);
}

.device-btn:hover {
  background: rgba(0, 0, 0, 0.8);
}

.pre-call-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: white;
}

.pre-call-info h3 {
  margin: 0 0 20px;
  font-size: 24px;
}

.participant-info {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 40px;
}

.participant {
  flex: 1;
  text-align: center;
}

.avatar-placeholder {
  font-size: 48px;
  margin-bottom: 8px;
}

.vs-text {
  font-weight: 600;
  color: #666;
}

.pre-call-actions {
  display: flex;
  gap: 12px;
  flex-direction: column;
}

.btn-start {
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-start:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.btn-start:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  padding: 10px 20px;
  background: transparent;
  color: white;
  border: 1px solid #666;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-cancel:hover {
  border-color: #999;
}

/* Active consultation */
.consultation-active {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.video-grid {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  padding: 12px;
}

.video-container {
  position: relative;
  background: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
}

.video-stream {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-label {
  position: absolute;
  bottom: 12px;
  left: 12px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.video-container.local {
  grid-column: 2;
  grid-row: 1;
  max-height: 150px;
  align-self: end;
}

/* Controls */
.consultation-controls {
  background: #1a1a1a;
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.duration {
  color: white;
  font-size: 18px;
  font-weight: 600;
  min-width: 60px;
}

.call-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #333;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background: #444;
  transform: scale(1.1);
}

.action-btn.inactive {
  background: #c62828;
}

.action-btn.recording {
  background: #f57c00;
  animation: pulse 1.5s infinite;
}

.action-btn.end-call {
  background: #c62828;
}

.action-btn.end-call:hover {
  background: #a71c1c;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

/* Chat Panel */
.chat-panel {
  width: 300px;
  background: #1a1a1a;
  border-left: 1px solid #333;
  display: flex;
  flex-direction: column;
  color: white;
}

.chat-header {
  padding: 12px;
  border-bottom: 1px solid #333;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h4 {
  margin: 0;
  font-size: 14px;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 18px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.message {
  max-width: 90%;
  padding: 8px 12px;
  background: #333;
  border-radius: 8px;
  font-size: 12px;
}

.message.own {
  align-self: flex-end;
  background: #667eea;
}

.message-sender {
  margin: 0;
  font-weight: 600;
  font-size: 11px;
  opacity: 0.8;
}

.message-text {
  margin: 4px 0;
  font-size: 12px;
}

.message-time {
  margin: 0;
  font-size: 10px;
  opacity: 0.6;
}

.chat-input {
  padding: 8px;
  border-top: 1px solid #333;
  display: flex;
  gap: 6px;
}

.chat-input input {
  flex: 1;
  padding: 6px;
  background: #333;
  border: 1px solid #444;
  border-radius: 4px;
  color: white;
  font-size: 12px;
}

.chat-input button {
  padding: 6px 12px;
  background: #667eea;
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  font-size: 11px;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 24px;
  max-width: 400px;
  width: 90%;
}

.modal-content h3 {
  margin-top: 0;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 6px;
  font-size: 12px;
}

.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-family: inherit;
  resize: none;
  box-sizing: border-box;
}

.modal-actions {
  display: flex;
  gap: 8px;
  margin-top: 24px;
}

.btn-confirm {
  flex: 1;
  padding: 10px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

.btn-confirm:hover {
  background: #5568d3;
}

@media (max-width: 768px) {
  .pre-call {
    grid-template-columns: 1fr;
  }

  .video-grid {
    grid-template-columns: 1fr;
  }

  .video-container.local {
    grid-column: 1;
    max-height: 120px;
  }

  .chat-panel {
    position: fixed;
    right: 0;
    bottom: 0;
    width: 280px;
    height: 300px;
  }
}
</style>
