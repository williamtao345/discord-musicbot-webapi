<script setup>
import { Music, Play, X } from 'lucide-vue-next'

defineProps({
  index: {
    type: Number,
    required: true
  },
  track: {
    type: Object,
    required: true
  },
  playing: {
    type: Boolean,
    default: false
  }
})

defineEmits(['play', 'remove'])
</script>

<template>
  <div class="queue-item" :class="{ playing }">
    <div class="item-index">
      <span class="item-num">{{ index }}</span>
      <Play class="item-play" :size="16" @click="$emit('play', track)" />
    </div>
    <div class="item-art">
      <Music :size="20" />
    </div>
    <div class="item-info">
      <div class="item-title">{{ track.title }}</div>
      <div class="item-artist">{{ track.artist }}</div>
    </div>
    <div class="item-source">{{ track.source }}</div>
    <div class="item-duration">{{ track.duration }}</div>
    <button class="item-remove" @click="$emit('remove', track)">
      <X :size="16" />
    </button>
  </div>
</template>

<style scoped>
.queue-item {
  display: grid;
  grid-template-columns: 50px 60px 1fr 100px 80px 40px;
  align-items: center;
  gap: 16px;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: grab;
  transition: background 0.1s;
  user-select: none;
}

.queue-item:active {
  cursor: grabbing;
}

.queue-item:hover {
  background: var(--bg-accent);
}

.queue-item:hover .item-num {
  opacity: 0;
}

.queue-item:hover .item-play {
  opacity: 1;
}

.queue-item:hover .item-remove {
  opacity: 1;
}

.queue-item.playing {
  background: rgba(88, 101, 242, 0.15);
}

.queue-item.playing .item-title {
  color: var(--blurple);
}

.item-index {
  position: relative;
  text-align: center;
}

.item-num {
  font-size: 14px;
  color: var(--text-muted);
  transition: opacity 0.1s;
}

.item-play {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0;
  color: var(--header-primary);
  transition: opacity 0.1s;
  cursor: pointer;
}

.item-art {
  width: 48px;
  height: 48px;
  background: var(--bg-accent);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
}

.item-info {
  min-width: 0;
}

.item-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--header-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 2px;
}

.item-artist {
  font-size: 13px;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-source {
  font-size: 13px;
  color: var(--text-muted);
}

.item-duration {
  font-size: 13px;
  color: var(--text-muted);
  text-align: right;
}

.item-remove {
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  border-radius: 4px;
  color: var(--text-muted);
  cursor: pointer;
  opacity: 0;
  transition: all 0.1s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-remove:hover {
  background: rgba(237, 66, 69, 0.2);
  color: var(--red);
}

@media (max-width: 900px) {
  .queue-item {
    grid-template-columns: 40px 50px 1fr 60px 40px;
  }
  .item-source {
    display: none;
  }
}
</style>
