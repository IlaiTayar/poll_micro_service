import httpx
from typing import Optional

from fastapi import HTTPException

from api.internal_api.user_service.model.user import User
from database import config


async def _get_from_user_service(url: str, params: Optional[dict] = None) -> dict:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url, params=params)
    except (httpx.ConnectError, httpx.TimeoutException) as err:
        raise HTTPException(
            status_code=503,
            detail=f"User Service unavailable: {err}"
        )
    except httpx.HTTPError as err:
        raise HTTPException(
            status_code=502,
            detail=f"Error communicating with User Service: {err}"
        )

    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail=response.json().get("detail", "User not found")
        )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=502,
            detail="User Service returned an error"
        )

    return response.json()


async def get_user_by_id(user_id: int) -> User:
    url: str = f"{config.USER_SERVICE_URL}/get/"
    data = await _get_from_user_service(url, {"user_id": user_id})
    return User(user_id=data["user_id"], is_registered=data["is_registered"])