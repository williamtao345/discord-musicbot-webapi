<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { AlertTriangle, Settings, X } from 'lucide-vue-next'
import { getApiKey } from '../api/config'

const router = useRouter()
const isVisible = ref(false)

onMounted(() => {
  const apiKey = getApiKey()
  if (!apiKey) {
    isVisible.value = true
  }
})

const goToSettings = () => {
  isVisible.value = false
  router.push('/settings')
}

const dismiss = () => {
  isVisible.value = false
}
</script>

<template>
  <Teleport to="body">
    <div v-if="isVisible" class="popup-overlay" @click.self="dismiss">
      <div class="popup">
        <button class="close-btn" @click="dismiss">
          <X :size="20" />
        </button>

        <div class="popup-icon">
          <AlertTriangle :size="48" />
        </div>

        <h2 class="popup-title">API Key Required</h2>

        <p class="popup-message">
          No API key is configured. You need to set an API key to connect to the music bot backend.
        </p>

        <button class="settings-btn" @click="goToSettings">
          <Settings :size="18" />
          Go to Settings
        </button>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.popup-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.popup {
  position: relative;
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 32px;
  max-width: 400px;
  width: 90%;
  text-align: center;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: var(--text-normal);
  background: var(--bg-tertiary);
}

.popup-icon {
  color: var(--yellow, #faa61a);
  margin-bottom: 16px;
}

.popup-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--header-primary);
  margin-bottom: 12px;
}

.popup-message {
  font-size: 14px;
  color: var(--text-muted);
  line-height: 1.6;
  margin-bottom: 24px;
}

.settings-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: var(--blurple);
  border: none;
  border-radius: 8px;
  color: var(--header-primary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.settings-btn:hover {
  background: var(--blurple-dark, #4752c4);
}
</style>
