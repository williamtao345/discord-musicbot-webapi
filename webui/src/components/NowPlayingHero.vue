<script setup>
import { computed } from 'vue'
import { Music, Clock, Video } from 'lucide-vue-next'
import { usePlayerStore } from '../composables/usePlayerStore'

const { currentTrack, playerState } = usePlayerStore()

const formatDuration = (seconds) => {
  if (!seconds) return '--:--'
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const title = computed(() => currentTrack.value?.title || 'Nothing Playing')
const artist = computed(() => currentTrack.value?.author || currentTrack.value?.channel || 'Unknown')
const duration = computed(() => formatDuration(currentTrack.value?.duration))
const source = computed(() => {
  const url = currentTrack.value?.url || ''
  if (url.includes('youtube')) return 'YouTube'
  if (url.includes('bilibili')) return 'Bilibili'
  if (url.includes('soundcloud')) return 'SoundCloud'
  return 'Unknown'
})
</script>

<template>
  <div class="now-playing-hero">
    <div class="hero-art">
      <Music :size="56" />
    </div>
    <div class="hero-info">
      <div class="hero-label">Now Playing</div>
      <h1 class="hero-title">{{ title }}</h1>
      <p class="hero-artist">{{ artist }}</p>
      <div class="hero-meta">
        <span>
          <Clock :size="14" />
          {{ duration }}
        </span>
        <span>
          <Video :size="14" />
          {{ source }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.now-playing-hero {
  background: linear-gradient(135deg, var(--blurple) 0%, #eb459e 100%);
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 32px;
  display: flex;
  align-items: center;
  gap: 24px;
  position: relative;
  overflow: hidden;
}

.now-playing-hero::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 400px;
  height: 400px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.now-playing-hero::after {
  content: '';
  position: absolute;
  bottom: -60%;
  left: -10%;
  width: 300px;
  height: 300px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 50%;
}

.hero-art {
  width: 140px;
  height: 140px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  color: var(--header-primary);
}

.hero-info {
  flex: 1;
  position: relative;
  z-index: 1;
}

.hero-label {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  opacity: 0.9;
  margin-bottom: 8px;
  font-weight: 600;
}

.hero-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--header-primary);
  margin-bottom: 4px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.hero-artist {
  font-size: 16px;
  opacity: 0.9;
  margin-bottom: 16px;
}

.hero-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 13px;
  opacity: 0.8;
}

.hero-meta span {
  display: flex;
  align-items: center;
  gap: 6px;
}
</style>
