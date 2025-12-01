<script setup>
import { ref, watch } from 'vue'
import {
  ChevronLeft,
  Edit3,
  Plus,
  Loader,
  Save,
  X,
  RefreshCw,
  Music
} from 'lucide-vue-next'
import draggable from 'vuedraggable'
import PlaylistTrackItem from './PlaylistTrackItem.vue'

const props = defineProps({
  playlist: { type: Object, required: true },
  metadataCache: { type: Object, required: true },
  loadingMetadata: { type: Set, required: true },
  loading: { type: Boolean, default: false },
  error: { type: String, default: null }
})

const emit = defineEmits([
  'back',
  'rename',
  'add-track',
  'remove-track',
  'reorder',
  'clear-error'
])

// Local state
const editingName = ref(false)
const editedName = ref('')
const newTrackUrl = ref('')
const isAddingTrack = ref(false)
const localTracks = ref([])
const hasReordered = ref(false)

// Watch for playlist changes to sync local tracks
watch(
  () => props.playlist?.tracks,
  (newTracks) => {
    if (newTracks) {
      localTracks.value = [...newTracks]
      hasReordered.value = false
    }
  },
  { immediate: true }
)

// Name editing
function startEditing() {
  editingName.value = true
  editedName.value = props.playlist?.name || ''
}

async function saveEditedName() {
  if (!editedName.value.trim() || editedName.value === props.playlist?.name) {
    editingName.value = false
    return
  }
  emit('rename', editedName.value.trim())
  editingName.value = false
}

function cancelEditing() {
  editingName.value = false
  editedName.value = ''
}

// Track operations
async function handleAddTrack() {
  if (!newTrackUrl.value.trim()) return
  isAddingTrack.value = true
  try {
    await emit('add-track', newTrackUrl.value.trim())
    newTrackUrl.value = ''
  } finally {
    isAddingTrack.value = false
  }
}

function handleRemoveTrack(index) {
  emit('remove-track', index)
}

// Reordering
function onDragEnd() {
  hasReordered.value = true
}

function saveReorder() {
  if (!hasReordered.value) return
  const originalTracks = props.playlist.tracks
  const newOrder = localTracks.value.map(url => originalTracks.indexOf(url))
  emit('reorder', newOrder)
  hasReordered.value = false
}

function cancelReorder() {
  localTracks.value = [...props.playlist.tracks]
  hasReordered.value = false
}

// Helpers
function getTrackMetadata(index) {
  const cacheKey = `${props.playlist?.name}:${index}`
  return props.metadataCache[cacheKey] || null
}

function isTrackLoadingMetadata(index) {
  return props.loadingMetadata.has(index)
}
</script>

<template>
  <div class="playlist-editor">
    <!-- Header -->
    <div class="editor-header">
      <button class="back-btn" @click="emit('back')">
        <ChevronLeft :size="20" />
        Back
      </button>

      <div class="playlist-title-section" v-if="playlist">
        <template v-if="editingName">
          <input
            v-model="editedName"
            type="text"
            class="edit-name-input"
            @keyup.enter="saveEditedName"
            @keyup.escape="cancelEditing"
          />
          <button class="icon-btn save" @click="saveEditedName">
            <Save :size="16" />
          </button>
          <button class="icon-btn cancel" @click="cancelEditing">
            <X :size="16" />
          </button>
        </template>
        <template v-else>
          <h1 class="editor-title">{{ playlist.name }}</h1>
          <button class="icon-btn" @click="startEditing" title="Rename">
            <Edit3 :size="16" />
          </button>
        </template>
      </div>

      <div class="track-count" v-if="playlist">
        {{ playlist.track_count }} tracks
      </div>
    </div>

    <!-- Reorder controls -->
    <div v-if="hasReordered" class="reorder-controls">
      <span>You have unsaved changes</span>
      <button class="save-btn" @click="saveReorder">
        <Save :size="16" />
        Save Order
      </button>
      <button class="cancel-btn" @click="cancelReorder">
        <X :size="16" />
        Cancel
      </button>
    </div>

    <!-- Add track -->
    <div class="add-track">
      <input
        v-model="newTrackUrl"
        type="text"
        placeholder="Add URL or search query..."
        @keyup.enter="handleAddTrack"
        :disabled="isAddingTrack"
      />
      <button @click="handleAddTrack" :disabled="isAddingTrack || !newTrackUrl.trim()">
        <Loader v-if="isAddingTrack" :size="16" class="spinning" />
        <Plus v-else :size="16" />
        Add
      </button>
    </div>

    <!-- Error message -->
    <div v-if="error" class="error-message">
      {{ error }}
      <button @click="emit('clear-error')" class="dismiss-btn">&times;</button>
    </div>

    <!-- Loading state -->
    <div v-else-if="loading && !playlist" class="loading">
      <RefreshCw :size="32" class="spinning" />
      <p>Loading playlist...</p>
    </div>

    <!-- Track list -->
    <draggable
      v-else-if="localTracks.length"
      v-model="localTracks"
      item-key="url"
      handle=".drag-handle"
      class="track-list"
      @end="onDragEnd"
    >
      <template #item="{ element: url, index }">
        <PlaylistTrackItem
          :url="url"
          :index="index"
          :metadata="getTrackMetadata(index)"
          :is-loading-metadata="isTrackLoadingMetadata(index)"
          @remove="handleRemoveTrack"
        />
      </template>
    </draggable>

    <!-- Empty state -->
    <div v-else class="empty-state">
      <Music :size="64" />
      <h2>No tracks</h2>
      <p>Add some tracks to this playlist.</p>
    </div>
  </div>
</template>

<style scoped>
.playlist-editor {
  width: 100%;
}

.editor-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.editor-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 24px;
  font-weight: 700;
  color: var(--header-primary);
  margin: 0;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  background: var(--bg-accent);
  border: none;
  border-radius: 4px;
  color: var(--text-normal);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn:hover {
  background: var(--bg-tertiary);
}

.playlist-title-section {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.edit-name-input {
  font-size: 24px;
  font-weight: 700;
  background: var(--bg-secondary);
  border: 1px solid var(--blurple);
  border-radius: 4px;
  color: var(--header-primary);
  padding: 4px 12px;
  width: 300px;
}

.icon-btn {
  width: 32px;
  height: 32px;
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

.icon-btn:hover {
  background: var(--bg-accent);
  color: var(--header-primary);
}

.icon-btn.save:hover {
  background: var(--green);
}

.icon-btn.cancel:hover {
  background: var(--red);
}

.track-count {
  font-size: 14px;
  color: var(--text-muted);
  margin-left: auto;
}

.reorder-controls {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--bg-accent);
  border-radius: 8px;
  margin-bottom: 16px;
}

.reorder-controls span {
  color: var(--text-normal);
  font-size: 14px;
}

.save-btn,
.cancel-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.save-btn {
  background: var(--green);
  color: var(--header-primary);
  margin-left: auto;
}

.save-btn:hover {
  filter: brightness(1.1);
}

.cancel-btn {
  background: var(--bg-tertiary);
  color: var(--text-normal);
}

.cancel-btn:hover {
  background: var(--red);
  color: var(--header-primary);
}

.add-track {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
}

.add-track input {
  flex: 1;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border: none;
  border-radius: 4px;
  color: var(--text-normal);
  font-size: 14px;
}

.add-track input::placeholder {
  color: var(--text-muted);
}

.add-track button {
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

.add-track button:hover:not(:disabled) {
  background: var(--blurple-hover);
}

.add-track button:disabled {
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

.track-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
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
