import client from './client'

export const playbackApi = {
  play: () => client.post('/playback/play'),
  pause: () => client.post('/playback/pause'),
  resume: () => client.post('/playback/resume'),
  skip: () => client.post('/playback/skip'),
  stop: () => client.post('/playback/stop')
}
