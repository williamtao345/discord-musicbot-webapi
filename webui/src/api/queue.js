import client from './client'

export const queueApi = {
  add: (query) => client.post('/queue/add', { query }),
  remove: (index) => client.delete(`/queue/${index}`),
  shuffle: () => client.post('/queue/shuffle'),
  clear: () => client.delete('/queue')
}
