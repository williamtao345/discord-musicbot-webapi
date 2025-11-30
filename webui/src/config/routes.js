import { Music, Search, HardDrive, Settings } from 'lucide-vue-next'

export const routes = [
  { path: '/', label: 'Now Playing', icon: Music },
  { path: '/search', label: 'Search', icon: Search },
  { path: '/cache', label: 'Cached Songs', icon: HardDrive },
  { path: '/settings', label: 'Settings', icon: Settings },
]

// For components that need dividers (NavSidebar)
export const navItems = [
  routes[0],
  { divider: true },
  routes[1],
  routes[2],
  { divider: true },
  routes[3],
]

// For simple path-to-label lookup (MainHeader)
export const routeLabels = Object.fromEntries(
  routes.map(r => [r.path, r.label])
)
