"""
Settings control routes - Volume, loop modes, etc.
"""
from fastapi import APIRouter, Depends, Body
from typing import Optional

from ..schemas import SuccessResponse, VolumeRequest, LoopRequest
from ..auth import verify_api_key
from ..dependencies import get_player

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.put("/volume", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def set_volume(request: VolumeRequest):
    """
    Set playback volume (0.0 to 2.0, where 1.0 is 100%)
    """
    player = get_player(request.guild_id)

    try:
        player.volume = request.volume
        percentage = int(request.volume * 100)
        return SuccessResponse(message=f"Volume set to {percentage}%")
    except Exception as e:
        return SuccessResponse(success=False, message=f"Failed to set volume: {str(e)}")


@router.get("/volume", dependencies=[Depends(verify_api_key)])
async def get_volume(guild_id: Optional[int] = None):
    """
    Get current playback volume
    """
    player = get_player(guild_id)
    percentage = int(player.volume * 100)
    return {"volume": player.volume, "percentage": percentage}


@router.put("/loop", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def set_loop(request: LoopRequest):
    """
    Set loop modes (loop queue and/or loop current song)
    """
    player = get_player(request.guild_id)

    try:
        messages = []

        if request.loop_queue is not None:
            if hasattr(player, 'loopqueue'):
                player.loopqueue = request.loop_queue
                status = "enabled" if request.loop_queue else "disabled"
                messages.append(f"Loop queue {status}")

        if request.loop_song is not None:
            if hasattr(player, 'repeatsong'):
                player.repeatsong = request.loop_song
                status = "enabled" if request.loop_song else "disabled"
                messages.append(f"Loop song {status}")

        if not messages:
            return SuccessResponse(success=False, message="No loop settings were changed")

        return SuccessResponse(message="; ".join(messages))

    except Exception as e:
        return SuccessResponse(success=False, message=f"Failed to set loop: {str(e)}")


@router.get("/loop", dependencies=[Depends(verify_api_key)])
async def get_loop(guild_id: Optional[int] = None):
    """
    Get current loop settings
    """
    player = get_player(guild_id)
    return {
        "loop_queue": getattr(player, 'loopqueue', False),
        "loop_song": getattr(player, 'repeatsong', False)
    }
