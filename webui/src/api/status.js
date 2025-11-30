import client from './client'

export const statusApi = {
  getStatus: () => client.get('/status'),
  getPlayer: () => client.get('/status/player'),
  getQueue: () => client.get('/status/queue')
}
