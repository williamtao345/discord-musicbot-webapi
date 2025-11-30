<script setup>
import { computed } from 'vue'
import { Music, Shuffle, SkipBack, Play, Pause, SkipForward, Repeat, Volume2 } from 'lucide-vue-next'
import SliderTrack from './SliderTrack.vue'
import { usePlayerStore } from '../composables/usePlayerStore'
import { usePlayback } from '../composables/usePlayback'
import { useQueue } from '../composables/useQueue'

const { currentTrack, isPlaying, volume, progress, loopQueue } = usePlayerStore()
const { togglePlay, skip, setVolume, setLoop, seek, isActionPending } = usePlayback()
const { shuffleQueue } = useQueue()

// Format time from seconds to mm:ss
const formatTime = (seconds) => {
  if (!seconds || isNaN(seconds)) return '0:00'
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const currentTime = computed(() => formatTime(progress.value))
const duration = computed(() => formatTime(currentTrack.value?.duration))
const progressPercent = computed(() => {
  if (!currentTrack.value?.duration || !progress.value) return 0
  return (progress.value / currentTrack.value.duration) * 100
})
const volumePercent = computed(() => Math.round((volume.value || 0.5) * 100))

const handleVolumeChange = (percent) => {
  setVolume(percent / 100)
}

const handleProgressChange = (percent) => {
  if (!currentTrack.value?.duration) return
  const position = (percent / 100) * currentTrack.value.duration
  seek(position)
}

const handleToggleLoop = () => {
  setLoop(!loopQueue.value, null)
}
</script>

<template>
  <div class="now-playing-bar">
    <!-- Left: Track Info -->
    <div class="np-left">
      <div class="np-art">
        <Music :size="24" />
      </div>
      <div class="np-info">
        <div class="np-title">{{ currentTrack?.title || 'Nothing playing' }}</div>
        <div class="np-artist">{{ currentTrack?.author || currentTrack?.channel || '' }}</div>
      </div>
    </div>

    <!-- Center: Controls -->
    <div class="np-center">
      <div class="np-controls">
        <button
          class="np-btn"
          title="Shuffle Queue"
          @click="shuffleQueue"
        >
          <Shuffle :size="16" />
        </button>
        <button class="np-btn" title="Previous" disabled>
          <SkipBack :size="16" />
        </button>
        <button
          class="np-btn play"
          :title="isPlaying ? 'Pause' : 'Play'"
          :disabled="isActionPending"
          @click="togglePlay"
        >
          <Pause v-if="isPlaying" :size="16" />
          <Play v-else :size="16" />
        </button>
        <button class="np-btn" title="Next" :disabled="isActionPending" @click="skip">
          <SkipForward :size="16" />
        </button>
        <button
          class="np-btn"
          :class="{ active: loopQueue }"
          title="Loop Queue"
          @click="handleToggleLoop"
        >
          <Repeat :size="16" />
        </button>
      </div>
      <div class="np-progress">
        <span class="np-time">{{ currentTime }}</span>
        <SliderTrack :value="progressPercent" @change="handleProgressChange" />
        <span class="np-time">{{ duration }}</span>
      </div>
    </div>

    <!-- Right: Volume -->
    <div class="np-right">
      <button class="volume-btn">
        <Volume2 :size="18" />
      </button>
      <div class="volume-slider">
        <SliderTrack :value="volumePercent" @change="handleVolumeChange" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.now-playing-bar {
  position: fixed;
  bottom: 0;
  left: 72px;
  right: 0;
  height: 80px;
  background: var(--bg-secondary);
  border-top: 1px solid var(--bg-tertiary);
  display: grid;
  grid-template-columns: minmax(0, 1fr) 300px minmax(0, 1fr);
  align-items: center;
  padding: 0 16px;
  z-index: 100;
}

/* Left: Track Info */
.np-left {
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 0;
  overflow: hidden;
}

.np-art {
  width: 56px;
  height: 56px;
  background: var(--bg-accent);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
}

.np-info {
  min-width: 0;
}

.np-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--header-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 2px;
}

.np-title:hover {
  text-decoration: underline;
  cursor: pointer;
}

.np-artist {
  font-size: 12px;
  color: var(--text-muted);
}

.np-artist:hover {
  text-decoration: underline;
  cursor: pointer;
  color: var(--text-normal);
}

/* Center: Controls */
.np-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.np-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.np-btn {
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  border-radius: 50%;
  color: var(--text-normal);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.1s;
}

.np-btn:hover {
  color: var(--header-primary);
  transform: scale(1.1);
}

.np-btn.active {
  color: var(--blurple);
}

.np-btn.play {
  width: 36px;
  height: 36px;
  background: var(--header-primary);
  color: var(--bg-tertiary);
}

.np-btn.play:hover {
  transform: scale(1.06);
  background: var(--header-primary);
}

.np-progress {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  max-width: 500px;
}

.np-time {
  font-size: 11px;
  color: var(--text-muted);
  width: 40px;
  text-align: center;
  font-variant-numeric: tabular-nums;
}

/* Right: Volume */
.np-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
}

.volume-btn {
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.volume-btn:hover {
  color: var(--text-normal);
}

.volume-slider {
  width: 100px;
}

@media (max-width: 768px) {
  .now-playing-bar {
    left: 60px;
    grid-template-columns: minmax(0, 1fr) 300px minmax(0, 1fr);
  }
}
</style>
