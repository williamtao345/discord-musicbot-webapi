import { ref } from 'vue'
import { playbackApi, settingsApi } from '../api'
import { usePlayerStore } from './usePlayerStore'

export function usePlayback() {
  const { fetchStatus, isPlaying } = usePlayerStore()
  const isActionPending = ref(false)

  async function togglePlay() {
    isActionPending.value = true
    try {
      if (isPlaying.value) {
        await playbackApi.pause()
      } else {
        await playbackApi.resume()
      }
      await fetchStatus()
    } catch (err) {
      console.error('Playback toggle failed:', err)
    } finally {
      isActionPending.value = false
    }
  }

  async function play() {
    isActionPending.value = true
    try {
      await playbackApi.play()
      await fetchStatus()
    } catch (err) {
      console.error('Play failed:', err)
    } finally {
      isActionPending.value = false
    }
  }

  async function pause() {
    isActionPending.value = true
    try {
      await playbackApi.pause()
      await fetchStatus()
    } catch (err) {
      console.error('Pause failed:', err)
    } finally {
      isActionPending.value = false
    }
  }

  async function skip() {
    isActionPending.value = true
    try {
      await playbackApi.skip()
      await fetchStatus()
    } catch (err) {
      console.error('Skip failed:', err)
    } finally {
      isActionPending.value = false
    }
  }

  async function stop() {
    isActionPending.value = true
    try {
      await playbackApi.stop()
      await fetchStatus()
    } catch (err) {
      console.error('Stop failed:', err)
    } finally {
      isActionPending.value = false
    }
  }

  async function setVolume(vol) {
    try {
      await settingsApi.setVolume(vol)
      await fetchStatus()
    } catch (err) {
      console.error('Failed to set volume:', err)
    }
  }

  async function setLoop(loopQueue, loopSong) {
    try {
      await settingsApi.setLoop(loopQueue, loopSong)
      await fetchStatus()
    } catch (err) {
      console.error('Failed to set loop:', err)
    }
  }

  return {
    isActionPending,
    togglePlay,
    play,
    pause,
    skip,
    stop,
    setVolume,
    setLoop
  }
}
