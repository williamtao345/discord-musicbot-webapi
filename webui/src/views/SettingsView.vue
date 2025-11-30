<script setup>
import { ref, onMounted } from 'vue'
import { Key, Save, CheckCircle } from 'lucide-vue-next'

const apiKey = ref('')
const saved = ref(false)

const STORAGE_KEY = 'musicbot_api_key'

onMounted(() => {
  const storedKey = localStorage.getItem(STORAGE_KEY)
  if (storedKey) {
    apiKey.value = storedKey
  }
})

const saveApiKey = () => {
  localStorage.setItem(STORAGE_KEY, apiKey.value)
  saved.value = true

  // Reload page to apply new API key
  setTimeout(() => {
    window.location.reload()
  }, 500)
}
</script>

<template>
  <div class="settings-view">
    <section class="setting-section">
      <h2 class="section-title">API Configuration</h2>
      <p class="section-description">
        Enter the API key to authenticate with the music bot backend.
      </p>

      <div class="api-key-form">
        <div class="input-group">
          <Key :size="20" class="input-icon" />
          <input
            v-model="apiKey"
            type="password"
            class="api-key-input"
            placeholder="Enter API key..."
            @keydown.enter="saveApiKey"
          >
        </div>

        <button class="save-btn" @click="saveApiKey" :class="{ saved }">
          <CheckCircle v-if="saved" :size="18" />
          <Save v-else :size="18" />
          {{ saved ? 'Saved!' : 'Save' }}
        </button>
      </div>

      <p class="help-text">
        The API key is stored locally in your browser. Leave empty if the backend has no authentication configured.
      </p>
    </section>
  </div>
</template>

<style scoped>
.settings-view {
  max-width: 600px;
}

.setting-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--header-primary);
  margin-bottom: 8px;
}

.section-description {
  font-size: 14px;
  color: var(--text-muted);
  margin-bottom: 20px;
}

.api-key-form {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.input-group {
  flex: 1;
  position: relative;
}

.input-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
}

.api-key-input {
  width: 100%;
  padding: 12px 12px 12px 44px;
  background: var(--bg-secondary);
  border: 1px solid var(--bg-tertiary);
  border-radius: 8px;
  color: var(--text-normal);
  font-size: 14px;
  font-family: monospace;
}

.api-key-input::placeholder {
  color: var(--text-muted);
}

.api-key-input:focus {
  outline: none;
  border-color: var(--blurple);
}

.save-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: var(--blurple);
  border: none;
  border-radius: 8px;
  color: var(--header-primary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.save-btn:hover {
  background: var(--blurple-dark, #4752c4);
}

.save-btn.saved {
  background: var(--green);
}

.help-text {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.5;
}
</style>
