from typing import List

from exceptions.exception import question_already_exists_exception, question_not_found_exception
from model.base_model.question import Question
from model.request_model.question_request import QuestionRequest
from repository import question_repository
from service import poll_service


async def create_question(question: QuestionRequest):
    existing_poll = await poll_service.get_poll_by_id(question.poll_id)
    if isinstance(existing_poll, Exception):
        return existing_poll

    existing_text = await get_questions_by_text(question.question_text)
    for text in existing_text:
        if text.poll_id == question.poll_id:
            return question_already_exists_exception(question.poll_id, question.question_text)

    new_question_id = await question_repository.create_question(question)
    return f"new question created with id: {new_question_id}, for poll: {question.poll_id}."


async def update_question_by_id(question_id: int, question: QuestionRequest):
    existing_question = await get_question_by_id(question_id)
    if isinstance(existing_question, Exception):
        return existing_question

    existing_poll = await poll_service.get_poll_by_id(question.poll_id)
    if isinstance(existing_poll, Exception):
        return existing_poll

    same_question_text = existing_question.question_text == question.question_text
    same_poll = existing_question.poll_id == question.poll_id

    if not (same_question_text and same_poll):
        existing_text = await get_questions_by_text(question.question_text)
        for text in existing_text:
            if text.poll_id == question.poll_id and text.question_id != question_id:
                return question_already_exists_exception(question.poll_id, question.question_text)

    await question_repository.update_question_by_id(question_id, question)
    return f"question updated with id: {question_id}, for poll: {question.poll_id}"


async def get_question_by_id(question_id: int):
    question = await question_repository.get_question_by_id(question_id)
    if not question:
        return question_not_found_exception(question_id)
    return question


async def get_questions_by_text(question_text: str) -> List[Question]:
    return await question_repository.get_questions_by_text(question_text)
