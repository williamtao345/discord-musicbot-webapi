import client from './client'

export const cacheApi = {
  list: () => client.get('/cache/'),
  delete: (filename) => client.delete(`/cache/${encodeURIComponent(filename)}`)
}
