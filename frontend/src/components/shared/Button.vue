<template>
  <button :class="['btn', buttonClass, sizeClass, { 'is-loading': loading }]" :disabled="disabled || loading">
    <span v-if="loading" class="spinner"></span>
    <span v-else>
      <span v-if="icon" class="icon">{{ icon }}</span>
      <slot></slot>
    </span>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'danger', 'success', 'warning'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  icon: String,
  loading: Boolean,
  disabled: Boolean
})

const buttonClass = computed(() => `btn-${props.variant}`)
const sizeClass = computed(() => `btn-${props.size}`)
</script>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  font-family: inherit;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn:not(:disabled):hover {
  transform: translateY(-2px);
}

/* Sizes */
.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

.btn-md {
  padding: 10px 16px;
  font-size: 14px;
}

.btn-lg {
  padding: 12px 24px;
  font-size: 16px;
}

/* Variants */
.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
}

.btn-primary:not(:disabled):hover {
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: white;
  color: #667eea;
  border: 1px solid #667eea;
}

.btn-secondary:not(:disabled):hover {
  background: #f5f5f5;
}

.btn-danger {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
  color: white;
}

.btn-danger:not(:disabled):hover {
  box-shadow: 0 4px 16px rgba(255, 107, 107, 0.4);
}

.btn-success {
  background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
  color: white;
}

.btn-success:not(:disabled):hover {
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.4);
}

.btn-warning {
  background: linear-gradient(135deg, #ffa500 0%, #ff9800 100%);
  color: white;
}

.btn-warning:not(:disabled):hover {
  box-shadow: 0 4px 16px rgba(255, 165, 0, 0.4);
}

.icon {
  font-size: 1.1em;
}

.is-loading {
  pointer-events: none;
}

.spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
