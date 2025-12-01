<script setup>
import { ref } from 'vue'
import { ListMusic, Plus, Trash2, RefreshCw, Loader, Play } from 'lucide-vue-next'

const props = defineProps({
  playlists: { type: Array, required: true },
  loading: { type: Boolean, default: false },
  error: { type: String, default: null }
})

const emit = defineEmits(['select', 'create', 'delete', 'refresh', 'clear-error', 'queue'])

const newPlaylistName = ref('')
const isCreating = ref(false)
const queuingPlaylist = ref(null)

async function handleCreate() {
  if (!newPlaylistName.value.trim()) return
  isCreating.value = true
  try {
    await emit('create', newPlaylistName.value.trim())
    newPlaylistName.value = ''
  } finally {
    isCreating.value = false
  }
}

function handleDelete(name) {
  if (!confirm(`Delete playlist "${name}"?`)) return
  emit('delete', name)
}

async function handleQueue(name) {
  if (queuingPlaylist.value) return
  queuingPlaylist.value = name
  try {
    await emit('queue', name)
  } finally {
    queuingPlaylist.value = null
  }
}
</script>

<template>
  <div class="playlist-list-container">
    <!-- Header -->
    <div class="list-header">
      <h1 class="list-title">
        <ListMusic :size="24" />
        Playlists
      </h1>
      <button class="refresh-btn" @click="emit('refresh')" :disabled="loading">
        <RefreshCw :size="16" :class="{ spinning: loading }" />
        Refresh
      </button>
    </div>

    <!-- Create new playlist -->
    <div class="create-playlist">
      <input
        v-model="newPlaylistName"
        type="text"
        placeholder="New playlist name..."
        @keyup.enter="handleCreate"
        :disabled="isCreating"
      />
      <button @click="handleCreate" :disabled="isCreating || !newPlaylistName.trim()">
        <Loader v-if="isCreating" :size="16" class="spinning" />
        <Plus v-else :size="16" />
        Create
      </button>
    </div>

    <!-- Error message -->
    <div v-if="error" class="error-message">
      {{ error }}
      <button @click="emit('clear-error')" class="dismiss-btn">&times;</button>
    </div>

    <!-- Loading state -->
    <div v-else-if="loading && !playlists.length" class="loading">
      <RefreshCw :size="32" class="spinning" />
      <p>Loading playlists...</p>
    </div>

    <!-- Playlist list -->
    <div v-else-if="playlists.length" class="playlist-list">
      <div
        v-for="playlist in playlists"
        :key="playlist.name"
        class="playlist-item"
        @click="emit('select', playlist.name)"
      >
        <div class="playlist-icon">
          <ListMusic :size="20" />
        </div>
        <div class="playlist-info">
          <div class="playlist-name">{{ playlist.name }}</div>
          <div class="playlist-meta">
            {{ playlist.track_count ?? '?' }} tracks
          </div>
        </div>
        <button
          class="play-btn"
          @click.stop="handleQueue(playlist.name)"
          :disabled="queuingPlaylist === playlist.name"
          title="Add to queue"
        >
          <Loader v-if="queuingPlaylist === playlist.name" :size="16" class="spinning" />
          <Play v-else :size="16" />
        </button>
        <button
          class="delete-btn"
          @click.stop="handleDelete(playlist.name)"
          title="Delete playlist"
        >
          <Trash2 :size="16" />
        </button>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else class="empty-state">
      <ListMusic :size="64" />
      <h2>No playlists</h2>
      <p>Create a playlist to get started.</p>
    </div>
  </div>
</template>

<style scoped>
.playlist-list-container {
  width: 100%;
}

.list-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.list-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 24px;
  font-weight: 700;
  color: var(--header-primary);
  margin: 0;
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
  margin-left: auto;
}

.refresh-btn:hover:not(:disabled) {
  background: var(--blurple);
  color: var(--header-primary);
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.create-playlist {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
}

.create-playlist input {
  flex: 1;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border: none;
  border-radius: 4px;
  color: var(--text-normal);
  font-size: 14px;
}

.create-playlist input::placeholder {
  color: var(--text-muted);
}

.create-playlist button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: var(--blurple);
  border: none;
  border-radius: 4px;
  color: var(--header-primary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.create-playlist button:hover:not(:disabled) {
  background: var(--blurple-hover);
}

.create-playlist button:disabled {
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
  display: flex;
  align-items: center;
  padding: 16px;
  background: rgba(237, 66, 69, 0.1);
  color: var(--red);
  border-radius: 8px;
  margin-bottom: 16px;
}

.dismiss-btn {
  margin-left: auto;
  background: transparent;
  border: none;
  color: var(--red);
  font-size: 20px;
  cursor: pointer;
  padding: 0 8px;
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

.playlist-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.playlist-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border-radius: 8px;
  transition: background 0.2s;
  cursor: pointer;
}

.playlist-item:hover {
  background: var(--bg-tertiary);
}

.playlist-icon {
  width: 36px;
  height: 36px;
  background: var(--bg-accent);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  flex-shrink: 0;
}

.playlist-info {
  flex: 1;
  min-width: 0;
}

.playlist-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--header-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.playlist-meta {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}

.play-btn,
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
  flex-shrink: 0;
}

.play-btn:hover:not(:disabled) {
  background: var(--blurple);
  color: var(--header-primary);
}

.play-btn:disabled {
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
