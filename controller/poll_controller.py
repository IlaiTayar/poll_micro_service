from fastapi import APIRouter, HTTPException
from starlette import status

from model.request_model.poll_request import PollRequest
from model.response_model.poll_response import PollResponse
from service import poll_service


router: APIRouter = APIRouter(prefix="/poll", tags=["Poll"])


def _exception_handler(result):
    if isinstance(result, HTTPException):
        raise result
    return result


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_poll(poll: PollRequest) -> str:
    result = await poll_service.create_poll(poll)
    return _exception_handler(result)


@router.put("/update_name/{poll_id}", status_code=status.HTTP_200_OK)
async def update_poll_by_id(poll_id: int, poll: PollRequest) -> str:
    result = await poll_service.update_poll_by_id(poll_id, poll)
    return _exception_handler(result)


@router.get("/get/{poll_id}/details", response_model=PollResponse, status_code=status.HTTP_200_OK)
async def get_poll_by_id(poll_id: int) -> PollResponse:
    result = await poll_service.get_poll_by_id(poll_id)
    return _exception_handler(result)


@router.delete("/delete/{poll_id}", status_code=status.HTTP_200_OK)
async def delete_poll_by_id(poll_id: int) -> str:
    result = await poll_service.delete_poll_by_id(poll_id)
    return _exception_handler(result)