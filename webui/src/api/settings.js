import client from './client'

export const settingsApi = {
  getVolume: () => client.get('/settings/volume'),
  setVolume: (volume) => client.put('/settings/volume', { volume }),
  getLoop: () => client.get('/settings/loop'),
  setLoop: (loopQueue, loopSong) => client.put('/settings/loop', {
    loop_queue: loopQueue,
    loop_song: loopSong
  })
}
