<script setup>
import { GripVertical, Music, Loader, Trash2 } from 'lucide-vue-next'

const props = defineProps({
  url: { type: String, required: true },
  index: { type: Number, required: true },
  metadata: { type: Object, default: null },
  isLoadingMetadata: { type: Boolean, default: false }
})

const emit = defineEmits(['remove'])

function formatDuration(seconds) {
  if (!seconds) return ''
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}
</script>

<template>
  <div class="track-item">
    <div class="drag-handle">
      <GripVertical :size="16" />
    </div>
    <div class="track-index">{{ index + 1 }}</div>
    <div class="track-icon">
      <Music :size="16" />
    </div>
    <div class="track-info">
      <div class="track-title">
        <Loader
          v-if="isLoadingMetadata"
          :size="12"
          class="spinning inline-loader"
        />
        {{ metadata?.title || url }}
      </div>
      <div class="track-url" v-if="metadata?.title">
        {{ url }}
      </div>
    </div>
    <div class="track-duration" v-if="metadata?.duration">
      {{ formatDuration(metadata.duration) }}
    </div>
    <button
      class="delete-btn"
      @click="emit('remove', index)"
      title="Remove track"
    >
      <Trash2 :size="16" />
    </button>
  </div>
</template>

<style scoped>
.track-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border-radius: 8px;
  transition: background 0.2s;
}

.track-item:hover {
  background: var(--bg-tertiary);
}

.drag-handle {
  cursor: grab;
  color: var(--text-muted);
  padding: 4px;
}

.drag-handle:active {
  cursor: grabbing;
}

.track-index {
  width: 24px;
  text-align: center;
  font-size: 12px;
  color: var(--text-muted);
}

.track-icon {
  width: 32px;
  height: 32px;
  background: var(--bg-accent);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  flex-shrink: 0;
}

.track-info {
  flex: 1;
  min-width: 0;
}

.track-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--header-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.track-url {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.track-duration {
  font-size: 12px;
  color: var(--text-muted);
  padding: 0 8px;
}

.inline-loader {
  display: inline-block;
  margin-right: 6px;
  vertical-align: middle;
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

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

.delete-btn:hover {
  background: var(--red);
  color: var(--header-primary);
}
</style>
