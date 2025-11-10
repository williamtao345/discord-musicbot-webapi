"""
Pydantic schemas for API request/response models
"""
from typing import Optional, List
from pydantic import BaseModel, Field


# Entry/Song schemas
class SongInfo(BaseModel):
    """Information about a song/entry"""
    title: str
    url: Optional[str] = None
    duration: Optional[float] = None
    thumbnail: Optional[str] = None
    author: Optional[str] = None
    channel: Optional[str] = None
    position: Optional[int] = None


# Player state schemas
class PlayerState(BaseModel):
    """Current player state"""
    state: str  # PLAYING, PAUSED, STOPPED, WAITING, DEAD
    current_song: Optional[SongInfo] = None
    volume: float
    loop_queue: bool = False
    loop_song: bool = False
    progress: Optional[float] = None  # Current playback position in seconds


# Queue schemas
class QueueInfo(BaseModel):
    """Information about the queue"""
    entries: List[SongInfo]
    total_duration: Optional[float] = None
    total_entries: int


# Status schemas
class BotStatus(BaseModel):
    """Overall bot status"""
    bot_name: str
    connected_guilds: int
    player_state: PlayerState
    queue: QueueInfo


# Request schemas
class AddSongRequest(BaseModel):
    """Request to add a song to the queue"""
    query: str = Field(..., description="URL or search query")
    guild_id: Optional[int] = Field(None, description="Guild ID (required if bot is in multiple servers)")


class RemoveSongRequest(BaseModel):
    """Request to remove a song from the queue"""
    index: int = Field(..., description="Index of the song in the queue (0-based)")
    guild_id: Optional[int] = None


class VolumeRequest(BaseModel):
    """Request to set volume"""
    volume: float = Field(..., ge=0.0, le=2.0, description="Volume level (0.0 to 2.0)")
    guild_id: Optional[int] = None


class LoopRequest(BaseModel):
    """Request to set loop mode"""
    loop_queue: Optional[bool] = None
    loop_song: Optional[bool] = None
    guild_id: Optional[int] = None


class GuildRequest(BaseModel):
    """Request with guild ID"""
    guild_id: Optional[int] = None


# Response schemas
class SuccessResponse(BaseModel):
    """Generic success response"""
    success: bool = True
    message: str


class ErrorResponse(BaseModel):
    """Generic error response"""
    success: bool = False
    error: str
    detail: Optional[str] = None
