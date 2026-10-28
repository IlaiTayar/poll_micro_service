from typing import Union

from fastapi import APIRouter, HTTPException
from starlette import status

from model.base_model.poll import Poll, PollError
from model.request_model.poll_request import PollRequest
from service import poll_service


router: APIRouter = APIRouter(prefix="/poll",
                              tags=["Poll"])


def _exception_handler(result):
    if isinstance(result, PollError):

        if result == PollError.NOT_FOUND:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.value)

        if result == PollError.NAME_EXISTS:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=result.value)

    return result


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_poll(poll: PollRequest) -> str:
    result: Union[str, PollError] = await poll_service.create_poll(poll)

    return _exception_handler(result)


@router.put("/update_name/{poll_id}", status_code=status.HTTP_200_OK)
async def update_poll_by_id(poll_id: int, poll: PollRequest) -> str:
    result: Union[str, PollError] = await poll_service.update_poll_by_id(poll_id, poll)

    return _exception_handler(result)


@router.get("/get/{poll_id}", response_model=Poll, status_code=status.HTTP_200_OK)
async def get_poll_by_id(poll_id: int) -> Poll:
    result: Union[Poll, PollError] = await poll_service.get_poll_by_id(poll_id)
    return _exception_handler(result)














