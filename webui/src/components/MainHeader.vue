<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { routeLabels } from '../config/routes'
import { usePlayerStore } from '../composables/usePlayerStore'

const route = useRoute()
const { botName, playerState, error } = usePlayerStore()

const pageTitle = computed(() => {
  return routeLabels[route.path] || routeLabels['/']
})

const isConnected = computed(() => !error.value && playerState.value !== 'DEAD')
const statusText = computed(() => {
  if (error.value) return 'Disconnected'
  return botName.value
})
</script>

<template>
  <header class="main-header">
    <span class="header-title">{{ pageTitle }}</span>
    <div class="header-status" :class="{ disconnected: !isConnected }">
      <span class="status-dot"></span>
      {{ statusText }}
    </div>
  </header>
</template>

<style scoped>
.main-header {
  height: 48px;
  padding: 0 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid var(--bg-tertiary);
  box-shadow: 0 1px 0 rgba(0, 0, 0, 0.2);
  flex-shrink: 0;
}

.header-title {
  font-weight: 600;
  font-size: 16px;
  color: var(--header-primary);
}

.header-status {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--green);
}

.status-dot {
  width: 8px;
  height: 8px;
  background: var(--green);
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.header-status.disconnected {
  color: var(--red);
}

.header-status.disconnected .status-dot {
  background: var(--red);
  animation: none;
}
</style>
