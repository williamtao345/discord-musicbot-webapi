import { createRouter, createWebHistory } from 'vue-router'
import NowPlayingView from '../views/NowPlayingView.vue'
import SearchView from '../views/SearchView.vue'
import CacheView from '../views/CacheView.vue'
import PlaylistsView from '../views/PlaylistsView.vue'
import SettingsView from '../views/SettingsView.vue'

const routes = [
  {
    path: '/',
    name: 'now-playing',
    component: NowPlayingView
  },
  {
    path: '/search',
    name: 'search',
    component: SearchView
  },
  {
    path: '/cache',
    name: 'cache',
    component: CacheView
  },
  {
    path: '/playlists',
    name: 'playlists',
    component: PlaylistsView
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingsView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
