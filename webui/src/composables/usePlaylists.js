import { ref, reactive } from 'vue'
import { playlistsApi } from '../api'

// Module-level state (shared across components)
const playlists = ref([])
const currentPlaylist = ref(null)
const loading = ref(false)
const error = ref(null)
const metadataCache = reactive({})

export function usePlaylists() {
  // Fetch all playlists
  async function fetchPlaylists() {
    loading.value = true
    error.value = null
    try {
      const response = await playlistsApi.list()
      playlists.value = response.data.playlists || []
      return playlists.value
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // Fetch a specific playlist with tracks
  async function fetchPlaylist(name) {
    loading.value = true
    error.value = null
    try {
      const response = await playlistsApi.get(name)
      currentPlaylist.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // Create a new playlist
  async function createPlaylist(name) {
    loading.value = true
    error.value = null
    try {
      const response = await playlistsApi.create(name)
      await fetchPlaylists()
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // Delete a playlist
  async function deletePlaylist(name) {
    loading.value = true
    error.value = null
    try {
      const response = await playlistsApi.delete(name)
      await fetchPlaylists()
      if (currentPlaylist.value?.name === name) {
        currentPlaylist.value = null
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // Rename a playlist
  async function renamePlaylist(oldName, newName) {
    loading.value = true
    error.value = null
    try {
      const response = await playlistsApi.rename(oldName, newName)
      await fetchPlaylists()
      if (currentPlaylist.value?.name === oldName) {
        await fetchPlaylist(newName)
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // Add a track to a playlist
  async function addTrack(playlistName, url, index = null) {
    error.value = null
    try {
      const response = await playlistsApi.addTrack(playlistName, url, index)
      if (currentPlaylist.value?.name === playlistName) {
        await fetchPlaylist(playlistName)
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
      throw err
    }
  }

  // Remove a track from a playlist
  async function removeTrack(playlistName, index) {
    error.value = null
    try {
      const response = await playlistsApi.removeTrack(playlistName, index)
      if (currentPlaylist.value?.name === playlistName) {
        await fetchPlaylist(playlistName)
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
      throw err
    }
  }

  // Move a track within a playlist
  async function moveTrack(playlistName, fromIndex, toIndex) {
    error.value = null
    try {
      const response = await playlistsApi.moveTrack(playlistName, fromIndex, toIndex)
      if (currentPlaylist.value?.name === playlistName) {
        await fetchPlaylist(playlistName)
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
      throw err
    }
  }

  // Reorder tracks in a playlist
  async function reorderTracks(playlistName, newOrder) {
    error.value = null
    try {
      const response = await playlistsApi.reorderTracks(playlistName, newOrder)
      if (currentPlaylist.value?.name === playlistName) {
        await fetchPlaylist(playlistName)
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
      throw err
    }
  }

  // Fetch and cache metadata for a track
  async function fetchTrackMetadata(playlistName, index) {
    const cacheKey = `${playlistName}:${index}`

    // Return cached metadata if available
    if (metadataCache[cacheKey]) {
      return metadataCache[cacheKey]
    }

    try {
      const response = await playlistsApi.getTrackMetadata(playlistName, index)
      metadataCache[cacheKey] = response.data
      return response.data
    } catch (err) {
      console.error('Failed to fetch track metadata:', err)
      return null
    }
  }

  // Clear metadata cache for a playlist
  function clearMetadataCache(playlistName = null) {
    if (playlistName) {
      Object.keys(metadataCache).forEach(key => {
        if (key.startsWith(`${playlistName}:`)) {
          delete metadataCache[key]
        }
      })
    } else {
      Object.keys(metadataCache).forEach(key => delete metadataCache[key])
    }
  }

  // Queue a playlist for playback
  async function queuePlaylist(playlistName, options = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await playlistsApi.queuePlaylist(playlistName, options)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // Clear error
  function clearError() {
    error.value = null
  }

  return {
    // State
    playlists,
    currentPlaylist,
    loading,
    error,
    metadataCache,

    // Playlist operations
    fetchPlaylists,
    fetchPlaylist,
    createPlaylist,
    deletePlaylist,
    renamePlaylist,

    // Track operations
    addTrack,
    removeTrack,
    moveTrack,
    reorderTracks,

    // Metadata
    fetchTrackMetadata,
    clearMetadataCache,

    // Playback
    queuePlaylist,

    // Utils
    clearError,
  }
}
