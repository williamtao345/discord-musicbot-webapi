"""
Playback control routes - Play, pause, skip, stop operations
"""
from fastapi import APIRouter, Depends, Body
from typing import Optional

from ..schemas import SuccessResponse, GuildRequest
from ..auth import verify_api_key
from ..dependencies import get_player

router = APIRouter(prefix="/api/playback", tags=["playback"])


@router.post("/play", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def play(request: GuildRequest = Body(default=GuildRequest())):
    """
    Resume or start playback
    """
    player = get_player(request.guild_id)

    try:
        # If paused, resume
        if hasattr(player, 'is_paused') and player.is_paused:
            player.resume()
            return SuccessResponse(message="Playback resumed")
        # If stopped and queue has items, start playing
        elif player.playlist and len(player.playlist.entries) > 0:
            await player.play()
            return SuccessResponse(message="Playback started")
        else:
            return SuccessResponse(message="Nothing to play. Queue is empty.")
    except Exception as e:
        return SuccessResponse(success=False, message=f"Failed to start playback: {str(e)}")


@router.post("/pause", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def pause(request: GuildRequest = Body(default=GuildRequest())):
    """
    Pause playback
    """
    player = get_player(request.guild_id)

    try:
        player.pause()
        return SuccessResponse(message="Playback paused")
    except Exception as e:
        return SuccessResponse(success=False, message=f"Failed to pause: {str(e)}")


@router.post("/resume", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def resume(request: GuildRequest = Body(default=GuildRequest())):
    """
    Resume paused playback
    """
    player = get_player(request.guild_id)

    try:
        player.resume()
        return SuccessResponse(message="Playback resumed")
    except Exception as e:
        return SuccessResponse(success=False, message=f"Failed to resume: {str(e)}")


@router.post("/skip", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def skip(request: GuildRequest = Body(default=GuildRequest())):
    """
    Skip current song
    """
    player = get_player(request.guild_id)

    try:
        await player.skip()
        return SuccessResponse(message="Skipped to next song")
    except Exception as e:
        return SuccessResponse(success=False, message=f"Failed to skip: {str(e)}")


@router.post("/stop", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def stop(request: GuildRequest = Body(default=GuildRequest())):
    """
    Stop playback
    """
    player = get_player(request.guild_id)

    try:
        player.stop()
        return SuccessResponse(message="Playback stopped")
    except Exception as e:
        return SuccessResponse(success=False, message=f"Failed to stop: {str(e)}")
