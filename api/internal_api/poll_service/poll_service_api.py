import httpx
from fastapi import HTTPException

from database import config


async def _request_poll_service(method: str, url: str, *, json_body=None, params=None):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            if method == "GET":
                response = await client.get(url, params=params)
            elif method == "POST":
                response = await client.post(url, json=json_body)
            elif method == "PUT":
                response = await client.put(url, params=params, json=json_body)
            elif method == "DELETE":
                response = await client.delete(url, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        if exc.response is not None:
            status_code = exc.response.status_code
            if status_code == 404:
                try:
                    detail = exc.response.json().get("detail", "Resource not found")
                except ValueError:
                    detail = exc.response.text or "Resource not found"
                raise HTTPException(status_code=404, detail=detail) from exc
            if status_code == 409:
                try:
                    detail = exc.response.json().get("detail", "Conflict")
                except ValueError:
                    detail = exc.response.text or "Conflict"
                raise HTTPException(status_code=409, detail=detail) from exc
            if status_code in (400, 422):
                try:
                    detail = exc.response.json().get("detail", "Invalid request")
                except ValueError:
                    detail = exc.response.text or "Invalid request"
                raise HTTPException(status_code=status_code, detail=detail) from exc
        raise HTTPException(status_code=502, detail="Poll Service returned an error") from exc
    except (httpx.ConnectError, httpx.TimeoutException) as exc:
        raise HTTPException(status_code=503, detail="Poll Service is unavailable") from exc
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=502, detail="Invalid request to Poll Service") from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="Error communicating with Poll Service") from exc

    try:
        return response.json()
    except ValueError:
        return response.text


async def answer_poll_question(answer):
    url = f"{config.POLL_SERVICE_URL}/user_answer/create"
    payload = answer.model_dump() if hasattr(answer, "model_dump") else answer.dict()
    return await _request_poll_service("POST", url, json_body=payload)


async def update_answer(answer_id: int, answer):
    url = f"{config.POLL_SERVICE_URL}/user_answer/update/{answer_id}"
    payload = answer.model_dump() if hasattr(answer, "model_dump") else answer.dict()
    return await _request_poll_service("PUT", url, json_body=payload)


async def get_poll_info(poll_id: int):
    url = f"{config.POLL_SERVICE_URL}/poll/get/{poll_id}/details"
    return await _request_poll_service("GET", url)


async def delete_answer(answer_id: int):
    url = f"{config.POLL_SERVICE_URL}/user_answer/delete/{answer_id}"
    return await _request_poll_service("DELETE", url)


async def delete_answers_by_user(user_id: int) -> str:
    url = f"{config.POLL_SERVICE_URL}/user_answer/delete/user/{user_id}"
    return await _request_poll_service("DELETE", url)
