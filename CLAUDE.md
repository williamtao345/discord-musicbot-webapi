# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a fork of MusicBot (Discord music bot) with an added REST API and Vue.js web interface for remote control via HTTP. The bot plays music from YouTube and other services into Discord voice channels.

## Development Commands

### Running the Bot
```bash
python run.py                # Run the bot (includes Web API if enabled in config)
./run.sh                     # Alternative launcher script
```

### Web UI Development
```bash
cd webui
npm install                  # Install dependencies
npm run dev                  # Dev server with hot reload (proxies /api to localhost:8000)
npm run build               # Production build (outputs to webapi/static/)
```

### Code Formatting
```bash
black --line-length 88 --target-version py311 <file>  # Format Python code
```
Pre-commit hooks run Black automatically.

## Architecture

### Core Components

**Python Backend (`musicbot/`):**
- `bot.py` - Main MusicBot class, Discord client, command handling (~7000 lines)
- `player.py` - MusicPlayer class managing audio playback, FFmpeg streaming, progress tracking
- `playlist.py` - Queue management for playback entries
- `entry.py` - URLPlaylistEntry, StreamPlaylistEntry, LocalFilePlaylistEntry types
- `config.py` - Configuration parsing from `config/options.ini`
- `downloader.py` - yt-dlp wrapper for audio extraction

**Web API (`webapi/`):**
- FastAPI application initialized via `initialize_api(bot_instance, api_key)`
- `dependencies.py` - Provides `get_bot()` and `get_player(guild_id)` for route handlers
- `routes/` - Endpoint modules: status, playback, queue, settings, cache
- `main.py` - FastAPI app setup, CORS, SPA fallback routing
- API runs concurrently with Discord bot via uvicorn in `run.py`

**Web Interface (`webui/`):**
- Vue 3 + Vite SPA
- Built assets deployed to `webapi/static/`
- Polls backend every 2 seconds for live updates
- Components in `src/components/`, views in `src/views/`

### Key Integration Points

The Web API and bot run together:
1. `run.py` creates MusicBot instance
2. If `config.webapi_enabled`, imports FastAPI app and calls `initialize_api(bot, api_key)`
3. `uvicorn.Server` runs concurrently with `bot.run_musicbot()` via `asyncio.gather()`
4. API routes access bot via `dependencies.get_bot()` and `dependencies.get_player()`

### Audio Pipeline

URL → yt-dlp metadata extraction → Queue entry → Download to `audio_cache/` → FFmpeg PCM → Discord voice

## Configuration

Main config: `config/options.ini` (copy from `config/example_options.ini`)

WebAPI section:
```ini
[WebAPI]
Enabled = yes
Host = 0.0.0.0
Port = 8000
APIKey = your-secret-key
DashboardURL = http://your-domain:8000
```
