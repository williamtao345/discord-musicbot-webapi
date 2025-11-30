# MusicBot

[![GitHub stars](https://img.shields.io/github/stars/Just-Some-Bots/MusicBot.svg)](https://github.com/Just-Some-Bots/MusicBot/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Just-Some-Bots/MusicBot.svg)](https://github.com/Just-Some-Bots/MusicBot/network)
[![Python version](https://img.shields.io/badge/python-3.8%2C%203.7%2C%203.6-blue.svg)](https://python.org)
[![Discord](https://discordapp.com/api/guilds/129489631539494912/widget.png?style=shield)](https://discord.gg/bots)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

MusicBot is the original Discord music bot written for [Python](https://www.python.org "Python homepage") 3.8+, using the [discord.py](https://github.com/Rapptz/discord.py) library. It plays requested songs from YouTube and other services into a Discord server (or multiple servers). If the queue is empty, MusicBot will play a list of existing songs that is configurable. The bot features a permission system, allowing owners to restrict commands to certain people. MusicBot is capable of streaming live media into a voice channel (experimental).

![Main](https://i.imgur.com/FWcHtcS.png)

## Web API & Interface (New Feature)

This fork adds a REST API and web interface for remote bot control via HTTP.

### Web Interface

A modern Vue.js web interface is included and pre-built. When the bot starts with WebAPI enabled, visit `http://localhost:8000/` for the control panel.

**Features:**
- **Now Playing** - Real-time display of current track with progress bar
- **Playback Controls** - Play, pause, skip, stop, shuffle, loop
- **Queue Management** - View queue, remove tracks, shuffle, clear
- **Search/Add** - Add songs by URL or search query
- **Settings** - Configure API key for authentication
- **Cache Management** - View and delete cached audio files

The interface polls the backend every 2 seconds for live updates.

### REST API Endpoints

| Category | Endpoints |
|----------|-----------|
| **Playback** | `POST /api/playback/{play,pause,resume,skip,stop}` |
| **Queue** | `POST /api/queue/add`, `DELETE /api/queue/{index}`, `POST /api/queue/shuffle`, `DELETE /api/queue` |
| **Settings** | `GET/PUT /api/settings/volume`, `GET/PUT /api/settings/loop` |
| **Status** | `GET /api/status`, `GET /api/status/player`, `GET /api/status/queue` |
| **Cache** | `GET /api/cache/`, `DELETE /api/cache/{filename}` |
| **Docs** | `GET /docs` (interactive Swagger documentation) |

### Configuration

Add to `config/options.ini`:
```ini
[WebAPI]
Enabled = yes
Host = 0.0.0.0
Port = 8000
APIKey = your-secret-key  ; Leave empty for no authentication
```

**Options:**
- `Enabled` - Enable/disable the web API and interface
- `Host` - IP address to bind to (`0.0.0.0` for all interfaces)
- `Port` - Port number (default: 8000)
- `APIKey` - Optional API key for authentication (leave empty to disable auth)

### Running as a System Service

To run MusicBot as a systemd service (automatic startup and background operation):

1. **Check service status:**
   ```bash
   sudo systemctl status musicbot.service
   ```

2. **Start/Stop/Restart the service:**
   ```bash
   sudo systemctl start musicbot.service
   sudo systemctl stop musicbot.service
   sudo systemctl restart musicbot.service
   ```

3. **Enable/Disable auto-start on boot:**
   ```bash
   sudo systemctl enable musicbot.service
   sudo systemctl disable musicbot.service
   ```

4. **View logs:**
   ```bash
   sudo journalctl -u musicbot.service -f
   ```

The service file should be located at `/etc/systemd/system/musicbot.service`.

### How It Works: URL → Music Playback

1. **User Input** → Web interface or API receives URL
2. **Metadata Extraction** → `yt-dlp` fetches info (title, duration) without downloading
3. **Queue Addition** → Entry added to queue instantly (non-blocking)
4. **Playback Trigger** → Player gets next entry when ready
5. **Download** → Audio file downloaded to `audio_cache/` (cached for reuse)
6. **Streaming** → `FFmpeg` converts to PCM audio → Discord voice channel

**Key Features:**
- **Two-phase process:** Fast metadata extraction, background audio download
- **Smart caching:** Downloaded files stored in `audio_cache/` to avoid re-downloads
- **Event-driven:** Queue management decoupled from playback
- **Async/non-blocking:** Queue adds instantly, downloads happen in background

### Bug Fixes
- Fixed `await` on synchronous `player.play()` and `player.skip()` methods
- Fixed queue API tuple unpacking for `add_entry_from_info()`
- Removed invalid `player.playlist.loop` parameter from `extract_info()` call

## Setup
Setting up the MusicBot is relatively painless - just follow one of the [guides](https://just-some-bots.github.io/MusicBot/). After that, configure the bot to ensure its connection to Discord.

The main configuration file is `config/options.ini`, but it is not included by default. Simply make a copy of `example_options.ini` and rename it to `options.ini`. See [`example_options.ini`](./config/example_options.ini) for more information about configurations.

### Commands

There are many commands that can be used with the bot. Most notably, the `play <url>` command (preceded by your command prefix), which will download, process, and play a song from YouTube or a similar site. A full list of commands is available [here](https://just-some-bots.github.io/MusicBot/using/commands/ "Commands").

### Further reading

* [Support Discord server](https://discord.gg/bots)
* [Project license](LICENSE)
