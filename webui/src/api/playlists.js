import client from './client'

export const playlistsApi = {
  // Playlist CRUD
  list: () => client.get('/playlists'),
  get: (name) => client.get(`/playlists/${encodeURIComponent(name)}`),
  create: (name) => client.post('/playlists', { name }),
  delete: (name) => client.delete(`/playlists/${encodeURIComponent(name)}`),
  rename: (name, newName) => client.put(`/playlists/${encodeURIComponent(name)}`, { new_name: newName }),

  // Track operations
  addTrack: (name, url, index = null) => client.post(`/playlists/${encodeURIComponent(name)}/tracks`, { url, index }),
  removeTrack: (name, index) => client.delete(`/playlists/${encodeURIComponent(name)}/tracks/${index}`),
  replaceTrack: (name, index, newUrl) => client.put(`/playlists/${encodeURIComponent(name)}/tracks/${index}`, { new_url: newUrl }),
  moveTrack: (name, fromIndex, toIndex) => client.post(`/playlists/${encodeURIComponent(name)}/tracks/move`, { from_index: fromIndex, to_index: toIndex }),
  reorderTracks: (name, newOrder) => client.post(`/playlists/${encodeURIComponent(name)}/tracks/reorder`, { new_order: newOrder }),

  // Metadata
  getTrackMetadata: (name, index) => client.get(`/playlists/${encodeURIComponent(name)}/tracks/${index}/metadata`),

  // Playback
  queuePlaylist: (name, { shuffle = false, clearQueue = false } = {}) =>
    client.post(`/playlists/${encodeURIComponent(name)}/queue`, null, {
      params: { shuffle, clear_queue: clearQueue }
    }),
}
