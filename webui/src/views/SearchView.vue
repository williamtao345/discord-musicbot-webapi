<script setup>
import { ref } from 'vue'
import { Search, Plus, Loader, AlertCircle, CheckCircle } from 'lucide-vue-next'
import { useQueue } from '../composables/useQueue'

const searchQuery = ref('')
const { addSong, isAdding, addError, addSuccess, clearMessages } = useQueue()

const handleSubmit = async () => {
  if (!searchQuery.value.trim() || isAdding.value) return

  clearMessages()
  try {
    await addSong(searchQuery.value.trim())
    searchQuery.value = ''
    // Clear success message after 3 seconds
    setTimeout(() => clearMessages(), 3000)
  } catch (err) {
    // Error is already in addError
  }
}

const handleKeydown = (e) => {
  if (e.key === 'Enter') handleSubmit()
}
</script>

<template>
  <div class="search-view">
    <div class="search-container">
      <Search class="search-icon" :size="20" />
      <input
        v-model="searchQuery"
        type="text"
        class="search-input"
        placeholder="Paste a YouTube URL or search query..."
        @keydown="handleKeydown"
        :disabled="isAdding"
      >
      <button
        class="add-btn"
        @click="handleSubmit"
        :disabled="!searchQuery.trim() || isAdding"
      >
        <Loader v-if="isAdding" :size="18" class="spinner" />
        <Plus v-else :size="18" />
        Add
      </button>
    </div>

    <div v-if="addError" class="message error">
      <AlertCircle :size="16" />
      {{ addError }}
    </div>

    <div v-if="addSuccess" class="message success">
      <CheckCircle :size="16" />
      {{ addSuccess }}
    </div>

    <div class="search-empty" v-if="!searchQuery && !isAdding && !addError && !addSuccess">
      <div class="empty-icon">
        <Search :size="64" />
      </div>
      <h2 class="empty-title">Add music to the queue</h2>
      <p class="empty-description">
        Paste a URL from YouTube, Bilibili, or any platform supported by yt-dlp.
        You can also enter a search query.
      </p>
    </div>
  </div>
</template>

<style scoped>
.search-view {
  max-width: 800px;
}

.search-container {
  position: relative;
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
}

.search-input {
  flex: 1;
  padding: 14px 16px 14px 48px;
  background: var(--bg-secondary);
  border: none;
  border-radius: 8px;
  color: var(--text-normal);
  font-size: 16px;
}

.search-input::placeholder {
  color: var(--text-muted);
}

.search-input:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--blurple);
}

.search-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.add-btn {
  padding: 14px 24px;
  background: var(--blurple);
  border: none;
  border-radius: 8px;
  color: var(--header-primary);
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.add-btn:hover:not(:disabled) {
  background: var(--blurple-dark, #4752c4);
}

.add-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  font-size: 14px;
}

.message.error {
  background: rgba(237, 66, 69, 0.1);
  color: var(--red);
}

.message.success {
  background: rgba(87, 242, 135, 0.1);
  color: var(--green);
}

.search-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 60px 20px;
  color: var(--text-muted);
}

.empty-icon {
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--header-primary);
  margin-bottom: 8px;
}

.empty-description {
  font-size: 14px;
  max-width: 400px;
  line-height: 1.5;
}
</style>
