from typing import List

from exceptions.exception import question_already_exists_exception, question_not_found_exception, question_already_answered
from model.base_model.question import Question
from model.request_model.question_request import QuestionRequest
from model.response_model.qustion_response import QuestionResponse
from repository import question_repository
from service import poll_service, answer_option_service, user_answer_service


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

    existing_answers = await user_answer_service.get_answers_by_question(question_id)
    if existing_answers:
        return question_already_answered(question_id)

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


async def get_questions_by_poll(poll_id: int):
    existing_questions = await question_repository.get_questions_by_poll(poll_id)
    response = []

    for question in existing_questions:
        options = await answer_option_service.get_options_by_question(question.question_id)
        response.append(QuestionResponse(question_id=question.question_id,
                                         question_text=question.question_text,
                                         options=options))

    return response


async def delete_question_by_id(question_id: int):
    existing_question = await get_question_by_id(question_id)
    if isinstance(existing_question, Exception):
        return existing_question

    existing_answers = await user_answer_service.get_answers_by_question(question_id)
    for answer in existing_answers:
        await user_answer_service.delete_answer_by_id(answer.answer_id)

    existing_options = await answer_option_service.get_options_by_question(question_id)
    for option in existing_options:
        await answer_option_service.delete_option_by_id(option.option_id)

    await question_repository.delete_question_by_id(question_id)
    return f"question deleted with id: {question_id}"
