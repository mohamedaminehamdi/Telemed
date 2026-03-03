<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h2>{{ isLogin ? 'Login' : 'Sign Up' }}</h2>
        <p class="subtitle">
          {{ isLogin ? 'Welcome back' : 'Create an account to get started' }}
        </p>
      </div>

      <form @submit.prevent="handleSubmit" class="auth-form">
        <!-- Email field -->
        <div class="form-group">
          <label for="email">Email Address</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="your@email.com"
            class="form-input"
            required
          />
        </div>

        <!-- Password field -->
        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="••••••••"
            class="form-input"
            required
          />
        </div>

        <!-- Confirm password (signup only) -->
        <div v-if="!isLogin" class="form-group">
          <label for="password-confirm">Confirm Password</label>
          <input
            id="password-confirm"
            v-model="form.passwordConfirm"
            type="password"
            placeholder="••••••••"
            class="form-input"
            required
          />
        </div>

        <!-- Name fields (signup only) -->
        <div v-if="!isLogin" class="form-row">
          <div class="form-group">
            <label for="first-name">First Name</label>
            <input
              id="first-name"
              v-model="form.firstName"
              type="text"
              placeholder="John"
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label for="last-name">Last Name</label>
            <input
              id="last-name"
              v-model="form.lastName"
              type="text"
              placeholder="Doe"
              class="form-input"
            />
          </div>
        </div>

        <!-- Error message -->
        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <!-- Submit button -->
        <button type="submit" class="btn-submit" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          {{ isLogin ? 'Login' : 'Sign Up' }}
        </button>
      </form>

      <!-- Toggle login/signup -->
      <div class="auth-footer">
        <p>
          {{ isLogin ? "Don't have an account?" : 'Already have an account?' }}
          <button type="button" @click="toggleMode" class="link-button">
            {{ isLogin ? 'Sign Up' : 'Login' }}
          </button>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isLogin = ref(true)
const loading = ref(false)
const error = ref(null)

const form = ref({
  email: '',
  password: '',
  passwordConfirm: '',
  firstName: '',
  lastName: ''
})

const toggleMode = () => {
  isLogin.value = !isLogin.value
  error.value = null
  resetForm()
}

const resetForm = () => {
  form.value = {
    email: '',
    password: '',
    passwordConfirm: '',
    firstName: '',
    lastName: ''
  }
}

const handleSubmit = async () => {
  error.value = null
  loading.value = true

  try {
    if (isLogin.value) {
      await authStore.login(form.value.email, form.value.password)
    } else {
      await authStore.register({
        email: form.value.email,
        password: form.value.password,
        password_confirm: form.value.passwordConfirm,
        first_name: form.value.firstName,
        last_name: form.value.lastName
      })
      isLogin.value = true
      resetForm()
      error.value = 'Account created! Please log in.'
    }
    
    if (isLogin.value && authStore.isAuthenticated) {
      router.push('/dashboard')
    }
  } catch (err) {
    error.value = authStore.error || 'An error occurred'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.auth-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
  padding: 40px;
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.auth-header h2 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #333;
}

.subtitle {
  margin: 8px 0 0;
  font-size: 14px;
  color: #999;
}

.auth-form {
  margin-bottom: 24px;
}

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
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  color: #667eea;
  margin-bottom: 6px;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.error-message {
  padding: 12px;
  margin-bottom: 16px;
  background: #fee;
  border-left: 4px solid #f77;
  color: #c33;
  font-size: 13px;
  border-radius: 4px;
}

.btn-submit {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.auth-footer {
  text-align: center;
}

.auth-footer p {
  margin: 0;
  font-size: 13px;
  color: #666;
}

.link-button {
  margin-left: 4px;
  background: none;
  border: none;
  color: #667eea;
  font-weight: 600;
  cursor: pointer;
  font-size: 13px;
  transition: color 0.3s ease;
}

.link-button:hover {
  color: #764ba2;
  text-decoration: underline;
}

@media (max-width: 600px) {
  .auth-card {
    margin: 16px;
    padding: 24px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
