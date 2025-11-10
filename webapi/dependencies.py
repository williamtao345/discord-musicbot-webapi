"""
Dependencies for API routes - provides access to bot instance
"""
from fastapi import HTTPException, status
from typing import Optional

# Global reference to the MusicBot instance
_bot_instance = None


def set_bot_instance(bot):
    """Set the global bot instance"""
    global _bot_instance
    _bot_instance = bot


def get_bot():
    """
    Dependency to get the bot instance

    Returns:
        The MusicBot instance

    Raises:
        HTTPException: If bot is not available
    """
    if _bot_instance is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Bot is not initialized"
        )
    return _bot_instance


def get_player(guild_id: Optional[int] = None):
    """
    Get the player for a specific guild

    Args:
        guild_id: Optional guild ID. If None and bot is in exactly one guild, uses that guild.

    Returns:
        MusicPlayer instance for the guild

    Raises:
        HTTPException: If guild_id is required but not provided, or player not found
    """
    bot = get_bot()

    # If no guild_id provided, try to infer from available guilds
    if guild_id is None:
        if len(bot.guilds) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot is not connected to any guilds"
            )
        elif len(bot.guilds) == 1:
            guild_id = bot.guilds[0].id
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Bot is in {len(bot.guilds)} guilds. Please specify guild_id."
            )

    # Find the guild
    guild = bot.get_guild(guild_id)
    if guild is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Guild {guild_id} not found"
        )

    # Get or create player for this guild
    try:
        player = bot.get_player_in(guild)
        return player
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get player: {str(e)}"
        )
