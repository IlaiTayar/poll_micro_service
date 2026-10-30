from typing import List

from api.internal_api.user_service import user_service_api
from api.internal_api.user_service.model.user import User
from exceptions.exception import user_not_registered_exception, cannot_update_answer_user_id_exception, \
    option_already_chosen_exception, answer_not_found_exception, question_not_found_exception, \
    answer_option_not_found_exception
from model.request_model.user_answer_request import UserAnswerRequest
from repository import user_answer_repository
from service import question_service, answer_option_service


async def create_answer(answer: UserAnswerRequest):
    existing_user: User = await user_service_api.get_user_by_id(answer.user_id)
    if not existing_user.is_registered:
        return user_not_registered_exception(answer.user_id)

    existing_question = await question_service.get_question_by_id(answer.question_id)
    if isinstance(existing_question, Exception):
        return existing_question

    if answer.option_id is not None:
        existing_option = await answer_option_service.get_option_by_id(answer.option_id)
        if isinstance(existing_option, Exception):
            return existing_option

    new_user_answer_id = await user_answer_repository.create_answer(answer)

    return f"new answer created with id: {new_user_answer_id} for user: {answer.user_id}, in poll: {existing_question.poll_id}"


async def update_answer_by_id(answer_id: int, answer: UserAnswerRequest):
    existing_answer = await get_answer_by_id(answer_id)
    if isinstance(existing_answer, Exception):
        return existing_answer

    existing_user: User = await user_service_api.get_user_by_id(answer.user_id)
    if not existing_user.is_registered:
        return user_not_registered_exception(answer.user_id)

    if existing_answer.user_id != answer.user_id:
        return cannot_update_answer_user_id_exception(answer_id)

    existing_question = await question_service.get_question_by_id(answer.question_id)
    if isinstance(existing_question, Exception):
        return existing_question

    if answer.option_id and existing_answer.option_id and existing_answer.option_id == answer.option_id:
        return option_already_chosen_exception(answer.user_id, answer.question_id, answer.option_id)

    await user_answer_repository.update_answer_by_id(answer_id, answer)
    return f"answer updated with id: {answer_id} for user: {answer.user_id}, in poll: {existing_question.poll_id}"


async def get_answer_by_id(answer_id: int):
    answer = await user_answer_repository.get_answer_by_id(answer_id)
    if answer is None:
        return answer_not_found_exception(answer_id)

    return answer


async def get_answers_by_question(question_id: int):
    answers = await user_answer_repository.get_answers_by_question(question_id)
    if not answers:
        return question_not_found_exception(question_id)

    return answers


async def get_answers_by_user(user_id: int):
    existing_user: User = await user_service_api.get_user_by_id(user_id)
    if not existing_user.is_registered:
        return user_not_registered_exception(user_id)

    answers = await user_answer_repository.get_answers_by_user(user_id)

    return answers


async def get_answers_by_option(option_id: int):
    answers = await user_answer_repository.get_answers_by_option(option_id)
    if not answers:
        return answer_option_not_found_exception(option_id)

    return answers


async def delete_answer_by_id(answer_id: int):
    existing_answer = await get_answer_by_id(answer_id)
    if isinstance(existing_answer, Exception):
        return existing_answer

    await user_answer_repository.delete_answer_by_id(answer_id)
    return f"answer deleted with id: {answer_id}"


