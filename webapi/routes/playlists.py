"""
Playlist management routes - CRUD operations for AutoPlaylists
"""
from fastapi import APIRouter, Depends, HTTPException, Path, status
from typing import Optional

from ..schemas import (
    SuccessResponse,
    PlaylistInfo,
    PlaylistDetail,
    PlaylistListResponse,
    TrackMetadata,
    CreatePlaylistRequest,
    RenamePlaylistRequest,
    AddTrackToPlaylistRequest,
    MoveTrackRequest,
    ReorderTracksRequest,
    ReplaceTrackRequest,
)
from ..auth import verify_api_key
from ..dependencies import get_bot, get_player

router = APIRouter(prefix="/api/playlists", tags=["playlists"])


@router.get("/", response_model=PlaylistListResponse, dependencies=[Depends(verify_api_key)])
async def list_playlists():
    """
    List all available playlists
    """
    bot = get_bot()

    try:
        playlist_mgr = bot.playlist_mgr
        # Refresh discovered playlists
        playlist_mgr.discover_playlists()

        playlists_info = []
        for name in playlist_mgr.playlist_names:
            pl = playlist_mgr.get_playlist(name)
            playlists_info.append(PlaylistInfo(
                name=name,
                filename=pl.filename,
                track_count=len(pl) if pl.loaded else None,
                loaded=pl.loaded,
            ))

        return PlaylistListResponse(
            playlists=playlists_info,
            total=len(playlists_info),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list playlists: {str(e)}",
        )


@router.post("/", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def create_playlist(request: CreatePlaylistRequest):
    """
    Create a new empty playlist
    """
    bot = get_bot()

    try:
        playlist_mgr = bot.playlist_mgr
        playlist = playlist_mgr.create_playlist(request.name)
        return SuccessResponse(message=f"Created playlist '{playlist._file.stem}'")
    except ValueError as e:
        return SuccessResponse(success=False, message=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create playlist: {str(e)}",
        )


@router.get("/{name}", response_model=PlaylistDetail, dependencies=[Depends(verify_api_key)])
async def get_playlist(
    name: str = Path(..., description="Playlist name"),
):
    """
    Get playlist details with all tracks
    """
    bot = get_bot()

    try:
        playlist_mgr = bot.playlist_mgr

        if not playlist_mgr.playlist_exists(name):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Playlist '{name}' not found",
            )

        pl = playlist_mgr.get_playlist(name)
        await pl.load(force=True)

        return PlaylistDetail(
            name=pl._file.stem,
            filename=pl.filename,
            tracks=list(pl.data),
            track_count=len(pl),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get playlist: {str(e)}",
        )


@router.delete("/{name}", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def delete_playlist(
    name: str = Path(..., description="Playlist name"),
):
    """
    Delete a playlist
    """
    bot = get_bot()

    try:
        playlist_mgr = bot.playlist_mgr
        playlist_mgr.delete_playlist(name)
        return SuccessResponse(message=f"Deleted playlist '{name}'")
    except ValueError as e:
        return SuccessResponse(success=False, message=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete playlist: {str(e)}",
        )


@router.put("/{name}", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def rename_playlist(
    request: RenamePlaylistRequest,
    name: str = Path(..., description="Current playlist name"),
):
    """
    Rename a playlist
    """
    bot = get_bot()

    try:
        playlist_mgr = bot.playlist_mgr
        playlist = playlist_mgr.rename_playlist(name, request.new_name)
        return SuccessResponse(message=f"Renamed playlist '{name}' to '{playlist._file.stem}'")
    except ValueError as e:
        return SuccessResponse(success=False, message=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to rename playlist: {str(e)}",
        )


@router.post("/{name}/tracks", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def add_track_to_playlist(
    request: AddTrackToPlaylistRequest,
    name: str = Path(..., description="Playlist name"),
):
    """
    Add a track to a playlist
    """
    bot = get_bot()

    try:
        playlist_mgr = bot.playlist_mgr

        if not playlist_mgr.playlist_exists(name):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Playlist '{name}' not found",
            )

        pl = playlist_mgr.get_playlist(name)
        await pl.load(force=True)

        if request.index is not None:
            await pl.insert_track(request.index, request.url)
            return SuccessResponse(message=f"Added track at index {request.index}")
        else:
            await pl.add_track(request.url)
            return SuccessResponse(message=f"Added track to playlist '{name}'")
    except IndexError as e:
        return SuccessResponse(success=False, message=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add track: {str(e)}",
        )


@router.delete("/{name}/tracks/{index}", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def remove_track_from_playlist(
    name: str = Path(..., description="Playlist name"),
    index: int = Path(..., ge=0, description="Track index (0-based)"),
):
    """
    Remove a track from a playlist by index
    """
    bot = get_bot()

    try:
        playlist_mgr = bot.playlist_mgr

        if not playlist_mgr.playlist_exists(name):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Playlist '{name}' not found",
            )

        pl = playlist_mgr.get_playlist(name)
        await pl.load(force=True)

        removed_url = await pl.remove_at_index(index)
        return SuccessResponse(message=f"Removed track: {removed_url}")
    except IndexError as e:
        return SuccessResponse(success=False, message=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to remove track: {str(e)}",
        )


@router.put("/{name}/tracks/{index}", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def replace_track_in_playlist(
    request: ReplaceTrackRequest,
    name: str = Path(..., description="Playlist name"),
    index: int = Path(..., ge=0, description="Track index (0-based)"),
):
    """
    Replace a track at a specific index
    """
    bot = get_bot()

    try:
        playlist_mgr = bot.playlist_mgr

        if not playlist_mgr.playlist_exists(name):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Playlist '{name}' not found",
            )

        pl = playlist_mgr.get_playlist(name)
        await pl.load(force=True)

        old_url = await pl.replace_track(index, request.new_url)
        return SuccessResponse(message=f"Replaced track: {old_url} -> {request.new_url}")
    except IndexError as e:
        return SuccessResponse(success=False, message=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to replace track: {str(e)}",
        )


@router.post("/{name}/tracks/move", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def move_track_in_playlist(
    request: MoveTrackRequest,
    name: str = Path(..., description="Playlist name"),
):
    """
    Move a track from one position to another
    """
    bot = get_bot()

    try:
        playlist_mgr = bot.playlist_mgr

        if not playlist_mgr.playlist_exists(name):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Playlist '{name}' not found",
            )

        pl = playlist_mgr.get_playlist(name)
        await pl.load(force=True)

        await pl.move_track(request.from_index, request.to_index)
        return SuccessResponse(message=f"Moved track from index {request.from_index} to {request.to_index}")
    except IndexError as e:
        return SuccessResponse(success=False, message=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to move track: {str(e)}",
        )


@router.post("/{name}/tracks/reorder", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def reorder_tracks_in_playlist(
    request: ReorderTracksRequest,
    name: str = Path(..., description="Playlist name"),
):
    """
    Reorder all tracks in a playlist
    """
    bot = get_bot()

    try:
        playlist_mgr = bot.playlist_mgr

        if not playlist_mgr.playlist_exists(name):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Playlist '{name}' not found",
            )

        pl = playlist_mgr.get_playlist(name)
        await pl.load(force=True)

        await pl.reorder(request.new_order)
        return SuccessResponse(message=f"Reordered {len(request.new_order)} tracks")
    except (IndexError, ValueError) as e:
        return SuccessResponse(success=False, message=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reorder tracks: {str(e)}",
        )


@router.get("/{name}/tracks/{index}/metadata", response_model=TrackMetadata, dependencies=[Depends(verify_api_key)])
async def get_track_metadata(
    name: str = Path(..., description="Playlist name"),
    index: int = Path(..., ge=0, description="Track index (0-based)"),
):
    """
    Fetch metadata for a track using yt-dlp
    """
    bot = get_bot()

    try:
        playlist_mgr = bot.playlist_mgr

        if not playlist_mgr.playlist_exists(name):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Playlist '{name}' not found",
            )

        pl = playlist_mgr.get_playlist(name)
        await pl.load(force=True)

        if index < 0 or index >= len(pl.data):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Index {index} out of bounds for playlist of length {len(pl.data)}",
            )

        url = pl.data[index]

        # Use yt-dlp to fetch metadata
        try:
            info = await bot.downloader.extract_info(url, download=False, process=False)
            if info:
                return TrackMetadata(
                    url=url,
                    title=info.get("title"),
                    duration=info.get("duration"),
                    thumbnail=info.get("thumbnail"),
                )
        except Exception:
            pass

        # Return basic info if metadata extraction fails
        return TrackMetadata(url=url)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch metadata: {str(e)}",
        )


@router.post("/{name}/queue", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def queue_playlist(
    name: str = Path(..., description="Playlist name"),
    guild_id: Optional[int] = None,
    shuffle: bool = False,
    clear_queue: bool = False,
):
    """
    Add all tracks from a playlist to the playback queue.

    - shuffle: Randomize track order before adding
    - clear_queue: Clear existing queue before adding
    """
    bot = get_bot()
    player = get_player(guild_id)

    try:
        playlist_mgr = bot.playlist_mgr

        if not playlist_mgr.playlist_exists(name):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Playlist '{name}' not found",
            )

        pl = playlist_mgr.get_playlist(name)
        await pl.load(force=True)

        if not pl.data:
            return SuccessResponse(success=False, message=f"Playlist '{name}' is empty")

        # Get tracks (optionally shuffled)
        tracks = list(pl.data)
        if shuffle:
            import random
            random.shuffle(tracks)

        # Clear existing queue if requested
        if clear_queue and player.playlist:
            player.playlist.clear()

        # Add each track to the queue
        added = 0
        failed = 0
        for url in tracks:
            try:
                info = await bot.downloader.extract_info(url, download=False, process=True)
                if info:
                    # Handle if yt-dlp returns a playlist
                    if 'entries' in info and info['entries']:
                        for entry_info in info['entries']:
                            if entry_info:
                                try:
                                    await player.playlist.add_entry_from_info(entry_info, head=False)
                                    added += 1
                                except Exception:
                                    failed += 1
                    else:
                        await player.playlist.add_entry_from_info(info, head=False)
                        added += 1
                else:
                    failed += 1
            except Exception as e:
                failed += 1
                continue

        message = f"Added {added} tracks from '{name}' to queue"
        if failed > 0:
            message += f" ({failed} failed)"

        return SuccessResponse(message=message)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to queue playlist: {str(e)}",
        )
