import { ref, computed, readonly } from 'vue'
import { statusApi } from '../api'

// Reactive state (module-level singleton)
const status = ref(null)
const isLoading = ref(false)
const error = ref(null)
let pollingInterval = null

// Computed properties
const currentTrack = computed(() => status.value?.player_state?.current_song || null)
const playerState = computed(() => status.value?.player_state?.state || 'STOPPED')
const isPlaying = computed(() => playerState.value === 'PLAYING')
const isPaused = computed(() => playerState.value === 'PAUSED')
const queue = computed(() => status.value?.queue?.entries || [])
const volume = computed(() => status.value?.player_state?.volume ?? 0.5)
const progress = computed(() => status.value?.player_state?.progress || 0)
const loopQueue = computed(() => status.value?.player_state?.loop_queue || false)
const loopSong = computed(() => status.value?.player_state?.loop_song || false)
const botName = computed(() => status.value?.bot_name || 'MusicBot')
const totalQueueDuration = computed(() => status.value?.queue?.total_duration || 0)
const queueLength = computed(() => status.value?.queue?.total_entries || 0)

export function usePlayerStore() {
  async function fetchStatus() {
    try {
      isLoading.value = true
      const response = await statusApi.getStatus()
      status.value = response.data
      error.value = null
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
    } finally {
      isLoading.value = false
    }
  }

  function startPolling(intervalMs = 2000) {
    stopPolling()
    fetchStatus()
    pollingInterval = setInterval(fetchStatus, intervalMs)
  }

  function stopPolling() {
    if (pollingInterval) {
      clearInterval(pollingInterval)
      pollingInterval = null
    }
  }

  return {
    // State (readonly to prevent direct mutation)
    status: readonly(status),
    isLoading: readonly(isLoading),
    error: readonly(error),

    // Computed
    currentTrack,
    playerState,
    isPlaying,
    isPaused,
    queue,
    volume,
    progress,
    loopQueue,
    loopSong,
    botName,
    totalQueueDuration,
    queueLength,

    // Actions
    fetchStatus,
    startPolling,
    stopPolling
  }
}
