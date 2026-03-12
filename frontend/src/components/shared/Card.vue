<template>
  <div :class="['card', cardClass]">
    <div v-if="$slots.header || title" class="card-header">
      <slot name="header">
        <h3 v-if="title">{{ title }}</h3>
      </slot>
    </div>

    <div class="card-body">
      <slot></slot>
    </div>

    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

defineProps({
  title: String,
  elevated: {
    type: Boolean,
    default: false
  },
  clickable: {
    type: Boolean,
    default: false
  }
})

const cardClass = computed(() => ({
  elevated: true,
  clickable: true
}))
</script>

<style scoped>
.card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.card.elevated {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.card.clickable {
  cursor: pointer;
}

.card.clickable:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  border-bottom: none;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.card-body {
  padding: 20px;
}

.card-footer {
  padding: 16px 20px;
  background: #f9f9f9;
  border-top: 1px solid #f0f0f0;
}

@media (max-width: 768px) {
  .card-header {
    padding: 16px;
  }

  .card-body {
    padding: 16px;
  }

  .card-footer {
    padding: 12px 16px;
  }
}
</style>
