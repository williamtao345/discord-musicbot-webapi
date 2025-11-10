"""
Queue management routes - Add, remove, shuffle, clear queue
"""
from fastapi import APIRouter, Depends, Body, HTTPException, status
from typing import Optional

from ..schemas import SuccessResponse, AddSongRequest, RemoveSongRequest, SongInfo
from ..auth import verify_api_key
from ..dependencies import get_bot, get_player

router = APIRouter(prefix="/api/queue", tags=["queue"])


@router.post("/add", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def add_song(request: AddSongRequest):
    """
    Add a song to the queue by URL or search query
    """
    bot = get_bot()
    player = get_player(request.guild_id)

    try:
        # Get the downloader from the bot
        if not hasattr(bot, 'downloader'):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Bot downloader not available"
            )

        # Extract info using yt-dlp
        info = await bot.downloader.extract_info(
            player.playlist.loop,
            request.query,
            download=False,
            process=True
        )

        if not info:
            return SuccessResponse(success=False, message="Could not extract song information")

        # Handle playlist vs single song
        if 'entries' in info and info['entries']:
            # It's a playlist
            num_songs = 0
            for entry in info['entries']:
                if entry:
                    try:
                        await player.playlist.add_entry_from_info(entry, head=False)
                        num_songs += 1
                    except Exception as e:
                        # Skip entries that fail
                        continue
            return SuccessResponse(message=f"Added {num_songs} songs from playlist to queue")
        else:
            # Single song
            entry = await player.playlist.add_entry_from_info(info, head=False)
            if entry:
                return SuccessResponse(message=f"Added '{entry.title}' to queue")
            else:
                return SuccessResponse(success=False, message="Failed to add song to queue")

    except Exception as e:
        return SuccessResponse(success=False, message=f"Failed to add song: {str(e)}")


@router.delete("/{index}", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def remove_song(
    index: int,
    guild_id: Optional[int] = None
):
    """
    Remove a song from the queue by index (0-based)
    """
    player = get_player(guild_id)

    try:
        if not player.playlist or len(player.playlist.entries) == 0:
            return SuccessResponse(success=False, message="Queue is empty")

        if index < 0 or index >= len(player.playlist.entries):
            return SuccessResponse(
                success=False,
                message=f"Invalid index. Queue has {len(player.playlist.entries)} entries (0-{len(player.playlist.entries)-1})"
            )

        entry = player.playlist.entries[index]
        player.playlist.delete_entry_at_index(index)
        return SuccessResponse(message=f"Removed '{entry.title}' from queue")

    except Exception as e:
        return SuccessResponse(success=False, message=f"Failed to remove song: {str(e)}")


@router.post("/shuffle", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def shuffle_queue(guild_id: Optional[int] = Body(None, embed=True)):
    """
    Shuffle the queue
    """
    player = get_player(guild_id)

    try:
        if not player.playlist or len(player.playlist.entries) == 0:
            return SuccessResponse(success=False, message="Queue is empty")

        player.playlist.shuffle()
        return SuccessResponse(message=f"Shuffled {len(player.playlist.entries)} songs")

    except Exception as e:
        return SuccessResponse(success=False, message=f"Failed to shuffle: {str(e)}")


@router.delete("", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def clear_queue(guild_id: Optional[int] = Body(None, embed=True)):
    """
    Clear the entire queue
    """
    player = get_player(guild_id)

    try:
        if not player.playlist:
            return SuccessResponse(message="Queue is already empty")

        count = len(player.playlist.entries)
        player.playlist.clear()
        return SuccessResponse(message=f"Cleared {count} songs from queue")

    except Exception as e:
        return SuccessResponse(success=False, message=f"Failed to clear queue: {str(e)}")
