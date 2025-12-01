"""
Main FastAPI application for Discord MusicBot Web API
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional
import logging
import os

from .routes import status, playback, queue, settings, cache, playlists
from . import dependencies, auth

log = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Discord MusicBot API",
    description="REST API for controlling Discord MusicBot",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(status.router)
app.include_router(playback.router)
app.include_router(queue.router)
app.include_router(settings.router)
app.include_router(cache.router)
app.include_router(playlists.router)

@app.get("/health")
async def health():
    """
    Health check endpoint
    """
    return {"status": "healthy"}


# Static files directory
static_dir = os.path.join(os.path.dirname(__file__), "static")

# SPA catch-all route - serves index.html for frontend routes
# This must be defined before mounting static files
@app.get("/{full_path:path}")
async def serve_spa(request: Request, full_path: str):
    """Serve the SPA for all non-API routes"""
    # Don't intercept API routes or other known paths
    if full_path.startswith("api/") or full_path in ("health", "docs", "redoc", "openapi.json"):
        return None

    # Check if requesting a static file (has extension)
    if "." in full_path.split("/")[-1]:
        file_path = os.path.join(static_dir, full_path)
        if os.path.exists(file_path):
            return FileResponse(file_path)

    # For all other routes, serve index.html (SPA fallback)
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)

    return {"detail": "Not Found"}

# Mount static files for assets
if os.path.exists(static_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")


def initialize_api(bot_instance, api_key: Optional[str] = None):
    """
    Initialize the Web API with bot instance and configuration

    Args:
        bot_instance: The MusicBot instance
        api_key: Optional API key for authentication
    """
    # Set bot instance for dependencies
    dependencies.set_bot_instance(bot_instance)

    # Set API key for authentication
    if api_key:
        auth.set_api_key(api_key)
        log.info("Web API authentication enabled")
    else:
        log.warning("Web API running without authentication - not recommended for production")

    log.info("Web API initialized successfully")
