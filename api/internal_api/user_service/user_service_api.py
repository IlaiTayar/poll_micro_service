import httpx

from fastapi import HTTPException

from api.internal_api.user_service.model.user import User
from database import config


async def get_user_info(user_id: int) -> User:
    url = f"{config.USER_SERVICE_URL}/user/get/{user_id}/details"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        if exc.response is not None and exc.response.status_code == 404:
            try:
                detail = exc.response.json().get("detail", "Resource not found")
            except ValueError:
                detail = exc.response.text or "Resource not found"
            raise HTTPException(status_code=404, detail=detail) from exc

        raise HTTPException(
            status_code=502,
            detail="Poll Service returned an error",
        ) from exc
    except (httpx.ConnectError, httpx.TimeoutException) as exc:
        raise HTTPException(
            status_code=503,
            detail="Poll Service is unavailable",
        ) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail="Error communicating with Poll Service",
        ) from exc

    return User(**response.json())