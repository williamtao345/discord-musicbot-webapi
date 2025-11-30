# MusicBot Web UI

A modern Vue.js web interface for controlling the Discord MusicBot.

## Features

- **Now Playing** - Real-time display of current track with progress bar
- **Playback Controls** - Play, pause, skip, stop, shuffle, loop
- **Queue Management** - View queue, drag to reorder, remove tracks, shuffle, clear
- **Search/Add** - Add songs by URL (YouTube, Bilibili, etc.) or search query
- **Settings** - Configure API key for authentication
- **Cache Management** - View and delete cached audio files

## Tech Stack

- **Vue 3** with Composition API (`<script setup>`)
- **Vue Router** for navigation
- **Axios** for API requests
- **Vite** for build tooling
- **Lucide Vue** for icons
- **vuedraggable** for drag-and-drop queue reordering

## Development

```bash
# Install dependencies
npm install

# Start dev server (with hot reload)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

The dev server runs on `http://localhost:5173` and proxies API requests to `http://localhost:8000`.

## Production

The frontend is pre-built and included in `webapi/static/`. When you run the bot with WebAPI enabled, the interface is automatically served at the same port as the API.

To rebuild after making changes:
```bash
npm run build
cp -r dist/* ../webapi/static/
```

## Project Structure

```
src/
├── api/                  # API client layer
│   ├── config.js         # API URL and key config
│   ├── client.js         # Axios instance with auth
│   ├── playback.js       # Playback endpoints
│   ├── queue.js          # Queue endpoints
│   ├── status.js         # Status endpoints
│   ├── settings.js       # Settings endpoints
│   └── cache.js          # Cache endpoints
├── composables/          # Vue composables (state management)
│   ├── usePlayerStore.js # Player state + polling
│   ├── usePlayback.js    # Playback actions
│   └── useQueue.js       # Queue actions
├── components/           # Reusable components
│   ├── PlaybackBar.vue   # Bottom playback control bar
│   ├── NowPlayingHero.vue# Current track display
│   ├── QueueSection.vue  # Queue list with drag-drop
│   ├── QueueItem.vue     # Individual queue item
│   ├── SliderTrack.vue   # Interactive slider
│   ├── NavSidebar.vue    # Navigation sidebar
│   └── MainHeader.vue    # Page header
├── views/                # Route views
│   ├── NowPlayingView.vue# Main playback view
│   ├── SearchView.vue    # Add songs
│   ├── SettingsView.vue  # API key config
│   └── CacheView.vue     # Cache management
├── config/
│   └── routes.js         # Route definitions
├── router/
│   └── index.js          # Vue Router config
├── App.vue               # Root component
└── main.js               # Entry point
```

## Configuration

The API key is stored in the browser's `localStorage`. Set it in the Settings page of the web interface.

If the backend has no API key configured, authentication is not required.
