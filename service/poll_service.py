from typing import Union, Optional

from model.base_model.poll import Poll, PollError
from model.request_model.poll_request import PollRequest
from repository import poll_repository



async def create_poll(poll: PollRequest) -> Union[str, PollError]:
    existing_poll: Union[Poll, PollError] = await get_poll_by_name(poll.poll_name)
    if not isinstance(existing_poll, PollError):
        return PollError.NAME_EXISTS

    created_id: int = await poll_repository.create_poll(poll)
    return f"poll {poll.poll_name} created with id: {created_id}."


async def update_poll_by_id(poll_id: int, poll: PollRequest) -> Union[str, PollError]:
    existing_poll: Union[Poll, PollError] = await get_poll_by_id(poll_id)
    if isinstance(existing_poll, PollError):
        return existing_poll

    await poll_repository.update_poll_by_id(poll_id, poll)
    return f"poll with id: {poll_id}, updated name from: {existing_poll.poll_name} to: {poll.poll_name}."


async def get_poll_by_id(poll_id: int) -> Union[Poll, PollError]:
    poll: Optional[Poll] = await poll_repository.get_poll_by_id(poll_id)
    if poll is None:
        return PollError.NOT_FOUND

    return poll


async def get_poll_by_name(poll_name: str) -> Union[Poll, PollError]:
    poll: Optional[Poll] = await poll_repository.get_poll_by_name(poll_name)
    if poll is None:
        return PollError.NOT_FOUND

    return poll