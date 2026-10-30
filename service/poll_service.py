from typing import Optional

from exceptions.exception import poll_name_exists_exception, poll_not_found_exception, poll_has_questions
from model.base_model.poll import Poll
from model.request_model.poll_request import PollRequest
from repository import poll_repository
from service import question_service


async def create_poll(poll: PollRequest):
    existing_poll = await get_polls_by_name(poll.poll_name)
    if existing_poll is not None:
        return poll_name_exists_exception(poll.poll_name)

    created_id = await poll_repository.create_poll(poll)
    return f"poll {poll.poll_name} created with id: {created_id}."


async def update_poll_by_id(poll_id: int, poll: PollRequest):
    existing_poll = await get_poll_by_id(poll_id)
    if isinstance(existing_poll, Exception):
        return existing_poll

    if existing_poll.poll_name != poll.poll_name:
        duplicate_poll = await get_polls_by_name(poll.poll_name)
        if duplicate_poll is not None and duplicate_poll.poll_id != poll_id:
            return poll_name_exists_exception(poll.poll_name)

    await poll_repository.update_poll_by_id(poll_id, poll)
    return f"poll with id: {poll_id}, updated name from: {existing_poll.poll_name} to: {poll.poll_name}."


async def get_poll_by_id(poll_id: int):
    poll = await poll_repository.get_poll_by_id(poll_id)
    if poll is None:
        return poll_not_found_exception(poll_id)
    return poll


async def get_polls_by_name(poll_name: str) -> Optional[Poll]:
    return await poll_repository.get_polls_by_name(poll_name)


async def delete_poll_by_id(poll_id: int):
    existing_poll = await get_poll_by_id(poll_id)
    if isinstance(existing_poll, Exception):
        return existing_poll

    existing_question = await question_service.get_questions_by_poll(poll_id)
    if existing_question:
        return poll_has_questions(poll_id)

    await poll_repository.delete_poll_by_id(poll_id)
    return f"poll with id: {poll_id} deleted."
