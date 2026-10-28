from typing import Union, List

from model.base_model.poll import PollError
from model.base_model.question import Question, QuestionError
from model.request_model.question_request import QuestionRequest
from repository import question_repository
from service import poll_service


async def create_question(question: QuestionRequest) -> Union[str, QuestionError, PollError]:
    existing_poll = await poll_service.get_poll_by_id(question.poll_id)
    if isinstance(existing_poll, PollError):
        return existing_poll

    existing_text = await get_question_by_text(question.question_text)
    if not isinstance(existing_text, QuestionError):
        for text in existing_text
            if text.poll_id == question.poll_id and text.question_text == question.question_text:
                return QuestionError.QUESTION_ALREADY_EXISTS

    new_question_id = await question_repository.create_question(question)
    return f"new question created with id: {new_question_id}, for poll: {question.poll_id}."


async def update_question_by_id(question_id: int, question: QuestionRequest) -> Union[str, QuestionError, PollError]:
    existing_question = await get_question_by_id(question_id)
    if isinstance(existing_question, QuestionError):
        return existing_question

    existing_poll = await poll_service.get_poll_by_id(question.poll_id)
    if isinstance(existing_poll, PollError):
        return existing_poll

    await question_repository.update_question_by_id(question_id, question)

    return f"question updated with id: {question_id}, for poll: {question.poll_id}"


async def get_question_by_id(question_id: int) -> Union[Question, QuestionError]:
    question = await question_repository.get_question_by_id(question_id)
    if not question:
        return QuestionError.QUESTION_NOT_FOUND

    return question


async def get_question_by_text(question_text: str) -> Union[List[Question], QuestionError]:
    question = await question_repository.get_question_by_text(question_text)
    if not question:
        return QuestionError.QUESTION_NOT_FOUND

    return question