"""
Status routes - Read-only endpoints for bot/player/queue status
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional

from ..schemas import BotStatus, PlayerState, QueueInfo, SongInfo
from ..auth import verify_api_key
from ..dependencies import get_bot, get_player

router = APIRouter(prefix="/api/status", tags=["status"])


def _entry_to_song_info(entry, position: Optional[int] = None) -> SongInfo:
    """Convert a playlist entry to SongInfo schema"""
    # Get video uploader/channel from metadata, not Discord user
    video_author = None
    if hasattr(entry, 'info'):
        video_author = entry.info.get("uploader") or entry.info.get("channel")

    return SongInfo(
        title=entry.title,
        url=getattr(entry, 'url', None),
        duration=entry.duration,
        thumbnail=getattr(entry, 'thumbnail', None),
        author=video_author,
        channel=video_author,  # Use same value for both fields
        position=position
    )


@router.get("", response_model=BotStatus, dependencies=[Depends(verify_api_key)])
async def get_status(guild_id: Optional[int] = Query(None, description="Guild ID")):
    """
    Get overall bot status including player state and queue
    """
    bot = get_bot()
    player = get_player(guild_id)

    # Get current song
    current_song = None
    if player.current_entry:
        current_song = _entry_to_song_info(player.current_entry)

    # Get player state
    player_state = PlayerState(
        state=player.state.name if hasattr(player.state, 'name') else str(player.state),
        current_song=current_song,
        volume=player.volume,
        loop_queue=getattr(player, 'loopqueue', False),
        loop_song=getattr(player, 'repeatsong', False),
        progress=getattr(player, 'progress', None)
    )

    # Get queue
    queue_entries = []
    if player.playlist:
        for i, entry in enumerate(player.playlist.entries):
            queue_entries.append(_entry_to_song_info(entry, position=i))

    total_duration = sum(e.duration for e in player.playlist.entries if e.duration) if player.playlist else 0

    queue_info = QueueInfo(
        entries=queue_entries,
        total_duration=total_duration,
        total_entries=len(queue_entries)
    )

    return BotStatus(
        bot_name=bot.user.name if bot.user else "Unknown",
        connected_guilds=len(bot.guilds),
        player_state=player_state,
        queue=queue_info
    )


@router.get("/player", response_model=PlayerState, dependencies=[Depends(verify_api_key)])
async def get_player_status(guild_id: Optional[int] = Query(None, description="Guild ID")):
    """
    Get current player state only
    """
    player = get_player(guild_id)

    current_song = None
    if player.current_entry:
        current_song = _entry_to_song_info(player.current_entry)

    return PlayerState(
        state=player.state.name if hasattr(player.state, 'name') else str(player.state),
        current_song=current_song,
        volume=player.volume,
        loop_queue=getattr(player, 'loopqueue', False),
        loop_song=getattr(player, 'repeatsong', False),
        progress=getattr(player, 'progress', None)
    )


@router.get("/queue", response_model=QueueInfo, dependencies=[Depends(verify_api_key)])
async def get_queue(guild_id: Optional[int] = Query(None, description="Guild ID")):
    """
    Get current queue
    """
    player = get_player(guild_id)

    queue_entries = []
    if player.playlist:
        for i, entry in enumerate(player.playlist.entries):
            queue_entries.append(_entry_to_song_info(entry, position=i))

    total_duration = sum(e.duration for e in player.playlist.entries if e.duration) if player.playlist else 0

    return QueueInfo(
        entries=queue_entries,
        total_duration=total_duration,
        total_entries=len(queue_entries)
    )
