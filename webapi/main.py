"""
Main FastAPI application for Discord MusicBot Web API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Optional
import logging
import os

from .routes import status, playback, queue, settings
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

@app.get("/health")
async def health():
    """
    Health check endpoint
    """
    return {"status": "healthy"}


# Mount static files (must be last to not override API routes)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


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
