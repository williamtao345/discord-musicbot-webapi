<script setup>
import { ref, onMounted } from 'vue'
import { HardDrive, Trash2, RefreshCw, Music, Plus, Loader } from 'lucide-vue-next'
import { cacheApi } from '../api'
import { useQueue } from '../composables/useQueue'

const { addSong } = useQueue()
const addingFilename = ref(null)

const cacheData = ref(null)
const isLoading = ref(false)
const error = ref(null)

const fetchCache = async () => {
  isLoading.value = true
  error.value = null
  try {
    const response = await cacheApi.list()
    cacheData.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || err.message
  } finally {
    isLoading.value = false
  }
}

const deleteFile = async (filename) => {
  try {
    await cacheApi.delete(filename)
    await fetchCache()
  } catch (err) {
    console.error('Failed to delete:', err)
  }
}

const addToQueue = async (song) => {
  if (addingFilename.value) return
  const query = song.url || song.filename
  addingFilename.value = song.filename
  try {
    await addSong(query)
  } catch (err) {
    console.error('Failed to add to queue:', err)
  } finally {
    addingFilename.value = null
  }
}

const formatSize = (mb) => {
  if (!mb) return '0 MB'
  if (mb >= 1024) return `${(mb / 1024).toFixed(2)} GB`
  return `${mb.toFixed(2)} MB`
}

onMounted(fetchCache)
</script>

<template>
  <div class="cache-view">
    <div class="cache-header">
      <h1 class="cache-title">
        <HardDrive :size="24" />
        Cached Songs
      </h1>
      <div class="cache-summary" v-if="cacheData">
        {{ cacheData.total_count || 0 }} files - {{ formatSize(cacheData.total_size_mb) }}
      </div>
      <button class="refresh-btn" @click="fetchCache" :disabled="isLoading">
        <RefreshCw :size="16" :class="{ spinning: isLoading }" />
        Refresh
      </button>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-else-if="isLoading && !cacheData" class="loading">
      <RefreshCw :size="32" class="spinning" />
      <p>Loading cache...</p>
    </div>

    <div v-else-if="cacheData?.cached_songs?.length" class="cache-list">
      <div
        v-for="song in cacheData.cached_songs"
        :key="song.filename"
        class="cache-item"
      >
        <div class="cache-icon">
          <Music :size="20" />
        </div>
        <div class="cache-info">
          <div class="cache-name">{{ song.title || song.filename }}</div>
          <div class="cache-meta">
            <span v-if="song.source">{{ song.source }}</span>
            <span>{{ formatSize(song.size_mb) }}</span>
          </div>
        </div>
        <button
          class="add-queue-btn"
          @click="addToQueue(song)"
          :disabled="addingFilename === song.filename"
          title="Add to queue"
        >
          <Loader v-if="addingFilename === song.filename" :size="16" class="spinning" />
          <Plus v-else :size="16" />
        </button>
        <button class="delete-btn" @click="deleteFile(song.filename)" title="Delete">
          <Trash2 :size="16" />
        </button>
      </div>
    </div>

    <div v-else class="empty-state">
      <HardDrive :size="64" />
      <h2>No cached songs</h2>
      <p>Songs will appear here after being downloaded.</p>
    </div>
  </div>
</template>

<style scoped>
.cache-view {
  max-width: 800px;
}

.cache-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.cache-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 24px;
  font-weight: 700;
  color: var(--header-primary);
  margin: 0;
}

.cache-summary {
  font-size: 14px;
  color: var(--text-muted);
  margin-left: auto;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--bg-accent);
  border: none;
  border-radius: 4px;
  color: var(--text-normal);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background: var(--blurple);
  color: var(--header-primary);
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.error-message {
  padding: 16px;
  background: rgba(237, 66, 69, 0.1);
  color: var(--red);
  border-radius: 8px;
  margin-bottom: 16px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: var(--text-muted);
  gap: 16px;
}

.cache-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.cache-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border-radius: 8px;
  transition: background 0.2s;
}

.cache-item:hover {
  background: var(--bg-tertiary);
}

.cache-icon {
  width: 40px;
  height: 40px;
  background: var(--bg-accent);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  flex-shrink: 0;
}

.cache-info {
  flex: 1;
  min-width: 0;
}

.cache-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--header-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 4px;
}

.cache-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: var(--text-muted);
}

.add-queue-btn,
.delete-btn {
  width: 36px;
  height: 36px;
  background: transparent;
  border: none;
  border-radius: 4px;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.add-queue-btn:hover:not(:disabled) {
  background: var(--blurple);
  color: var(--header-primary);
}

.add-queue-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.delete-btn:hover {
  background: var(--red);
  color: var(--header-primary);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 60px 20px;
  color: var(--text-muted);
}

.empty-state h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--header-primary);
  margin: 16px 0 8px;
}

.empty-state p {
  font-size: 14px;
}
</style>
