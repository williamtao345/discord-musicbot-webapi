"""
Authentication middleware for API key validation
"""
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from typing import Optional

# API Key header scheme
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Global variable to store the API key (will be set from config)
_api_key: Optional[str] = None


def set_api_key(key: str):
    """Set the API key for validation"""
    global _api_key
    _api_key = key


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Verify the API key from the request header

    Args:
        api_key: API key from X-API-Key header

    Returns:
        The validated API key

    Raises:
        HTTPException: If API key is missing or invalid
    """
    if _api_key is None:
        # API key not configured, allow access (for backwards compatibility)
        return "no-auth-configured"

    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Provide X-API-Key header.",
        )

    if api_key != _api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )

    return api_key
