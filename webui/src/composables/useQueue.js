import { ref } from 'vue'
import { queueApi } from '../api'
import { usePlayerStore } from './usePlayerStore'

export function useQueue() {
  const { fetchStatus } = usePlayerStore()
  const isAdding = ref(false)
  const addError = ref(null)
  const addSuccess = ref(null)

  async function addSong(query) {
    isAdding.value = true
    addError.value = null
    addSuccess.value = null
    try {
      const response = await queueApi.add(query)
      await fetchStatus()
      addSuccess.value = response.data?.message || 'Song added to queue'
      return response.data
    } catch (err) {
      addError.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      isAdding.value = false
    }
  }

  async function removeSong(index) {
    try {
      await queueApi.remove(index)
      await fetchStatus()
    } catch (err) {
      console.error('Failed to remove song:', err)
    }
  }

  async function shuffleQueue() {
    try {
      await queueApi.shuffle()
      await fetchStatus()
    } catch (err) {
      console.error('Failed to shuffle:', err)
    }
  }

  async function clearQueue() {
    try {
      await queueApi.clear()
      await fetchStatus()
    } catch (err) {
      console.error('Failed to clear queue:', err)
    }
  }

  function clearMessages() {
    addError.value = null
    addSuccess.value = null
  }

  return {
    isAdding,
    addError,
    addSuccess,
    addSong,
    removeSong,
    shuffleQueue,
    clearQueue,
    clearMessages
  }
}
