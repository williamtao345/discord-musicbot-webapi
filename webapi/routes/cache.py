"""
Cache management routes - View and delete cached songs
"""
from fastapi import APIRouter, Depends, HTTPException, Path
from typing import List, Optional
import json
import os
import pathlib

from ..schemas import SuccessResponse
from ..auth import verify_api_key
from ..dependencies import get_bot

router = APIRouter(prefix="/api/cache", tags=["cache"])


@router.get("/", dependencies=[Depends(verify_api_key)])
async def list_cached_songs():
    """
    List all cached songs in the audio_cache folder
    """
    bot = get_bot()
    cache_path = pathlib.Path(bot.config.audio_cache_path)

    if not cache_path.exists():
        return {
            "cached_songs": [],
            "total_count": 0,
            "total_size": 0
        }

    cached_songs = []
    total_size = 0

    try:
        for file_path in cache_path.iterdir():
            if file_path.is_file():
                # Skip metadata JSON files
                if file_path.name.endswith('.meta.json'):
                    continue

                stat = file_path.stat()
                file_size = stat.st_size
                total_size += file_size

                # Parse filename to extract info
                filename = file_path.name
                source = None
                video_id = None

                if filename.startswith("youtube-"):
                    source = "youtube"
                    parts = filename[8:].split("-", 1)
                    if parts:
                        video_id = parts[0]
                elif filename.startswith("BiliBili-"):
                    source = "bilibili"
                    parts = filename[9:].split("-", 1)
                    if parts:
                        video_id = parts[0]

                # Load metadata JSON if available
                metadata = None
                meta_file = file_path.with_suffix(file_path.suffix + ".meta.json")
                if meta_file.exists():
                    try:
                        with open(meta_file, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                    except Exception:
                        pass

                cached_songs.append({
                    "filename": filename,
                    "source": source,
                    "video_id": video_id,
                    "size": file_size,
                    "size_mb": round(file_size / (1024 * 1024), 2),
                    "modified_time": stat.st_mtime,
                    "extension": file_path.suffix,
                    # Add metadata fields
                    "title": metadata.get("title") if metadata else None,
                    "author": metadata.get("uploader") or metadata.get("channel") if metadata else None,
                    "duration": metadata.get("duration") if metadata else None,
                    "url": metadata.get("url") if metadata else None,
                    "has_metadata": metadata is not None,
                })

        # Sort by modified time (newest first)
        cached_songs.sort(key=lambda x: x["modified_time"], reverse=True)

        return {
            "cached_songs": cached_songs,
            "total_count": len(cached_songs),
            "total_size": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list cached songs: {str(e)}")


@router.delete("/{filename}", response_model=SuccessResponse, dependencies=[Depends(verify_api_key)])
async def delete_cached_song(
    filename: str = Path(..., description="The filename of the cached song to delete")
):
    """
    Delete a specific cached song by filename
    """
    bot = get_bot()
    cache_path = pathlib.Path(bot.config.audio_cache_path)

    # Security: Validate filename to prevent path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    file_path = cache_path / filename

    # Check if file exists
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {filename}")

    # Check if it's actually a file (not a directory)
    if not file_path.is_file():
        raise HTTPException(status_code=400, detail=f"Not a file: {filename}")

    try:
        # Get file size before deletion for the response
        file_size_mb = round(file_path.stat().st_size / (1024 * 1024), 2)

        # Delete the file
        file_path.unlink()

        return SuccessResponse(
            message=f"Successfully deleted '{filename}' ({file_size_mb} MB)"
        )

    except PermissionError:
        raise HTTPException(status_code=403, detail=f"Permission denied to delete file: {filename}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")
