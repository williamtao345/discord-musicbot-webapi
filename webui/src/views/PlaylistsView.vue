<script setup>
import { ref, onMounted } from 'vue'
import { usePlaylists } from '../composables/usePlaylists'
import PlaylistList from '../components/playlists/PlaylistList.vue'
import PlaylistEditor from '../components/playlists/PlaylistEditor.vue'

const {
  playlists,
  currentPlaylist,
  loading,
  error,
  metadataCache,
  fetchPlaylists,
  fetchPlaylist,
  createPlaylist,
  deletePlaylist,
  renamePlaylist,
  addTrack,
  removeTrack,
  reorderTracks,
  fetchTrackMetadata,
  clearMetadataCache,
  queuePlaylist,
  clearError
} = usePlaylists()

// Track which playlist is selected (null = show list)
const selectedPlaylist = ref(null)

// Track metadata loading states
const loadingMetadata = ref(new Set())

// Playlist list handlers
async function handleRefresh() {
  await fetchPlaylists()
}

async function handleSelect(name) {
  selectedPlaylist.value = name
  clearMetadataCache(name)
  await fetchPlaylist(name)
  loadVisibleMetadata()
}

async function handleCreate(name) {
  await createPlaylist(name)
}

async function handleDeletePlaylist(name) {
  await deletePlaylist(name)
  if (selectedPlaylist.value === name) {
    handleBack()
  }
}

async function handleQueuePlaylist(name) {
  await queuePlaylist(name)
}

// Editor handlers
function handleBack() {
  selectedPlaylist.value = null
  currentPlaylist.value = null
}

async function handleRename(newName) {
  await renamePlaylist(currentPlaylist.value.name, newName)
  selectedPlaylist.value = newName
}

async function handleAddTrack(url) {
  await addTrack(currentPlaylist.value.name, url)
  loadVisibleMetadata()
}

async function handleRemoveTrack(index) {
  await removeTrack(currentPlaylist.value.name, index)
  clearMetadataCache(currentPlaylist.value.name)
  loadVisibleMetadata()
}

async function handleReorder(newOrder) {
  await reorderTracks(currentPlaylist.value.name, newOrder)
  clearMetadataCache(currentPlaylist.value.name)
  loadVisibleMetadata()
}

// Metadata loading
async function loadVisibleMetadata() {
  if (!currentPlaylist.value) return
  const tracksToLoad = Math.min(currentPlaylist.value.tracks.length, 20)
  for (let i = 0; i < tracksToLoad; i++) {
    loadTrackMetadata(i)
  }
}

async function loadTrackMetadata(index) {
  if (!currentPlaylist.value) return
  const cacheKey = `${currentPlaylist.value.name}:${index}`
  if (metadataCache[cacheKey] || loadingMetadata.value.has(index)) return

  loadingMetadata.value.add(index)
  try {
    await fetchTrackMetadata(currentPlaylist.value.name, index)
  } finally {
    loadingMetadata.value.delete(index)
  }
}

onMounted(fetchPlaylists)
</script>

<template>
  <div class="playlists-view">
    <PlaylistList
      v-if="!selectedPlaylist"
      :playlists="playlists"
      :loading="loading"
      :error="error"
      @select="handleSelect"
      @create="handleCreate"
      @delete="handleDeletePlaylist"
      @refresh="handleRefresh"
      @clear-error="clearError"
      @queue="handleQueuePlaylist"
    />

    <PlaylistEditor
      v-else
      :playlist="currentPlaylist"
      :metadata-cache="metadataCache"
      :loading-metadata="loadingMetadata"
      :loading="loading"
      :error="error"
      @back="handleBack"
      @rename="handleRename"
      @add-track="handleAddTrack"
      @remove-track="handleRemoveTrack"
      @reorder="handleReorder"
      @clear-error="clearError"
    />
  </div>
</template>

<style scoped>
.playlists-view {
  max-width: 800px;
}
</style>
