from typing import Optional, Union, List

from exceptions.exception import (
    no_changes_submitted_exception,
    poll_name_exists_exception,
    poll_not_found_exception,
)
from model.base_model.poll import Poll

from model.request_model.poll_request import PollRequest
from model.response_model.poll_response import PollResponse
from model.response_model.qustion_response import QuestionResponse
from repository import poll_repository
from service import question_service


async def create_poll(poll: PollRequest):
    existing_poll: List[Poll] = await get_polls_by_name(poll.poll_name)
    if existing_poll is not None:
        return poll_name_exists_exception(poll.poll_name)

    created_id: Optional[int] = await poll_repository.create_poll(poll)
    return f"poll {poll.poll_name} created with id: {created_id}."


async def update_poll_by_id(poll_id: int, poll: PollRequest):
    existing_poll: Union[PollResponse, Exception] = await get_poll_by_id(poll_id)
    if isinstance(existing_poll, Exception):
        return existing_poll

    if existing_poll.poll_name == poll.poll_name:
        return no_changes_submitted_exception()

    duplicate_polls: List[Poll] = await get_polls_by_name(poll.poll_name)
    for duplicate_poll in duplicate_polls:
        if duplicate_poll.poll_id != poll_id:
            return poll_name_exists_exception(poll.poll_name)

    await poll_repository.update_poll_by_id(poll_id, poll)
    return f"poll with id: {poll_id}, updated name from: {existing_poll.poll_name} to: {poll.poll_name}."


async def get_poll_by_id(poll_id: int):
    poll: Optional[Poll] = await poll_repository.get_poll_by_id(poll_id)
    if poll is None:
        return poll_not_found_exception(poll_id)
    poll_questions: List[QuestionResponse] = await question_service.get_questions_by_poll(poll_id)
    return PollResponse(
        poll_id=poll_id,
        poll_name=poll.poll_name,
        questions=poll_questions,
    )


async def get_polls_by_name(poll_name: str):
    return await poll_repository.get_polls_by_name(poll_name)


async def delete_poll_by_id(poll_id: int):
    existing_poll: Union[PollResponse, Exception] = await get_poll_by_id(poll_id)
    if isinstance(existing_poll, Exception):
        return existing_poll

    questions: List[QuestionResponse] = await question_service.get_questions_by_poll(poll_id)
    for question in questions:
        await question_service.delete_question_by_id(question.question_id)

    await poll_repository.delete_poll_by_id(poll_id)
    return f"poll with id: {poll_id} deleted."