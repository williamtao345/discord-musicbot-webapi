<script setup>
import { ref, watch } from 'vue'
import { Shuffle, Trash2 } from 'lucide-vue-next'
import draggable from 'vuedraggable'
import QueueItem from './QueueItem.vue'
import { usePlayerStore } from '../composables/usePlayerStore'
import { useQueue } from '../composables/useQueue'

const { queue } = usePlayerStore()
const { removeSong, shuffleQueue, clearQueue } = useQueue()

// Local copy for vuedraggable (synced from store)
const localQueue = ref([])
const isDragging = ref(false)

// Sync from store when it changes
watch(queue, (newQueue) => {
  localQueue.value = [...newQueue]
}, { immediate: true })

const handlePlay = (track) => {
  // Playing a specific track from queue would require a backend endpoint
  console.log('Play:', track.title)
}

const handleRemove = async (track) => {
  // Use the position from the track (0-based index)
  if (track.position !== undefined) {
    await removeSong(track.position)
  }
}

const handleShuffle = () => shuffleQueue()
const handleClear = () => clearQueue()
</script>

<template>
  <section class="section">
    <div class="section-header">
      <h2 class="section-title">Up Next</h2>
      <div class="section-actions">
        <button class="section-btn" @click="handleShuffle">
          <Shuffle :size="16" />
          Shuffle
        </button>
        <button class="section-btn danger" @click="handleClear">
          <Trash2 :size="16" />
          Clear
        </button>
      </div>
    </div>
    <draggable
      v-model="localQueue"
      item-key="position"
      class="queue-list"
      :class="{ 'is-dragging': isDragging }"
      ghost-class="queue-item-ghost"
      drag-class="queue-item-drag"
      :filter="'.item-remove, .item-play'"
      :preventOnFilter="false"
      :forceFallback="true"
      @start="isDragging = true"
      @end="isDragging = false"
    >
      <template #item="{ element, index }">
        <QueueItem
          :index="index + 1"
          :track="element"
          @play="handlePlay"
          @remove="handleRemove"
        />
      </template>
    </draggable>
  </section>
</template>

<style scoped>
.section {
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--header-primary);
}

.section-actions {
  display: flex;
  gap: 8px;
}

.section-btn {
  padding: 8px 16px;
  background: var(--bg-accent);
  border: none;
  border-radius: 4px;
  color: var(--text-normal);
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.section-btn:hover {
  background: var(--blurple);
  color: var(--header-primary);
}

.section-btn.danger:hover {
  background: var(--red);
}

.queue-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

:deep(.queue-item-ghost) {
  opacity: 0.2;
}

.queue-list.is-dragging :deep(.queue-item:hover) {
  background: transparent;
}

.queue-list.is-dragging :deep(.queue-item:hover .item-remove) {
  opacity: 0;
}

.queue-list.is-dragging :deep(.queue-item:hover .item-play) {
  opacity: 0;
}

.queue-list.is-dragging :deep(.queue-item:hover .item-num) {
  opacity: 1;
}

:deep(.queue-item-drag) {
  opacity: 0.8 !important;
  background: var(--bg-secondary);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}
</style>
