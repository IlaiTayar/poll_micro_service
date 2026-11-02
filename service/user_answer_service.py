from typing import Union, List, Optional

from api.internal_api.user_service import user_service_api
from api.internal_api.user_service.model.user import User
from exceptions.exception import (
    answer_already_exists_exception,
    answer_not_found_exception,
    answer_option_not_found_exception,
    cannot_update_answer_user_id_exception,
    no_changes_submitted_exception,
    user_not_registered_exception,
)
from model.base_model.answer_option import AnswerOption
from model.base_model.question import Question
from model.base_model.user_answer import UserAnswer
from model.request_model.user_answer_request import UserAnswerRequest
from model.response_model.user_answer_response import UserAnswerResponse
from model.base_model.statistics import AnswerEntry
from repository import user_answer_repository
from service import answer_option_service, question_service


async def create_answer(answer: UserAnswerRequest):
    existing_user: User = await user_service_api.get_user_by_id(answer.user_id)
    if not existing_user.is_registered:
        return user_not_registered_exception(answer.user_id)

    existing_question: Union[Question, Exception] = await question_service.get_question_by_id(answer.question_id)
    if isinstance(existing_question, Exception):
        return existing_question

    if answer.option_id is not None:
        existing_option = await answer_option_service.get_option_by_id(answer.option_id)
        if isinstance(existing_option, Exception):
            return existing_option

        if existing_option.question_id != answer.question_id:
            return answer_option_not_found_exception(answer.option_id)

    existing_answers: List[UserAnswer] = await user_answer_repository.get_answers_by_user(answer.user_id)
    for existing_answer in existing_answers:
        if existing_answer.question_id == answer.question_id:
            return answer_already_exists_exception(answer.user_id, answer.question_id)

    new_user_answer_id: int = await user_answer_repository.create_answer(answer)
    return f"new answer created with id: {new_user_answer_id} for user: {answer.user_id}, in poll: {existing_question.poll_id}"


async def update_answer_by_id(answer_id: int, answer: UserAnswerRequest):
    existing_answer: Union[UserAnswer, Exception] = await get_answer_by_id(answer_id)
    if isinstance(existing_answer, Exception):
        return existing_answer

    if existing_answer.user_id != answer.user_id:
        return cannot_update_answer_user_id_exception(answer_id)

    existing_user: User = await user_service_api.get_user_by_id(answer.user_id)
    if not existing_user.is_registered:
        return user_not_registered_exception(answer.user_id)

    answer.user_id = existing_answer.user_id
    answer.question_id = existing_answer.question_id

    existing_question: Union[Question, Exception] = await question_service.get_question_by_id(answer.question_id)
    if isinstance(existing_question, Exception):
        return existing_question

    if answer.option_id is not None:
        existing_option = await answer_option_service.get_option_by_id(answer.option_id)
        if isinstance(existing_option, Exception):
            return existing_option

        if existing_option.question_id != answer.question_id:
            return answer_option_not_found_exception(answer.option_id)

    existing_answers: List[UserAnswer] = await user_answer_repository.get_answers_by_user(answer.user_id)
    for existing_answer_item in existing_answers:
        if existing_answer_item.answer_id != answer_id and existing_answer_item.question_id == answer.question_id:
            return answer_already_exists_exception(answer.user_id, answer.question_id)

    if (
        existing_answer.user_id == answer.user_id
        and existing_answer.question_id == answer.question_id
        and existing_answer.option_id == answer.option_id
    ):
        return no_changes_submitted_exception()

    await user_answer_repository.update_answer_by_id(answer_id, answer)
    return f"answer updated with id: {answer_id} for user: {answer.user_id}, in poll: {existing_question.poll_id}"


async def get_answer_by_id(answer_id: int):
    answer: Optional[UserAnswer] = await user_answer_repository.get_answer_by_id(answer_id)
    if answer is None:
        return answer_not_found_exception(answer_id)

    return answer


async def get_answers_by_question(question_id: int):
    existing_question: Union[Question, Exception] = await question_service.get_question_by_id(question_id)
    if isinstance(existing_question, Exception):
        return existing_question

    return await user_answer_repository.get_answers_by_question(question_id)


async def get_answers_by_user(user_id: int):
    answers: List[UserAnswer] = await user_answer_repository.get_answers_by_user(user_id)

    question_answer: dict[int, AnswerEntry] = {}
    for answer in answers:
        question = await question_service.get_question_by_id(answer.question_id)
        if isinstance(question, Exception):
            raise question

        option = None
        if answer.option_id is not None:
            option = await answer_option_service.get_option_by_id(answer.option_id)
            if isinstance(option, Exception):
                raise option
            if option.question_id != answer.question_id:
                raise answer_option_not_found_exception(answer.option_id)

        question_answer[answer.answer_id] = AnswerEntry(
            answer_id=answer.answer_id,
            question_id=answer.question_id,
            question_text=question.question_text,
            option_id=answer.option_id,
            option_text=option.option_text if option is not None else None,
        )

    return UserAnswerResponse(user_id=user_id, question_answer=question_answer)


async def get_answers_by_option(option_id: int):
    return await user_answer_repository.get_answers_by_option(option_id)


async def delete_answer_by_id(answer_id: int):
    existing_answer: Union[UserAnswer, Exception] = await get_answer_by_id(answer_id)
    if isinstance(existing_answer, Exception):
        return existing_answer

    await user_answer_repository.delete_answer_by_id(answer_id)
    return f"answer deleted with id: {answer_id}"


async def delete_answers_by_user(user_id: int):
    await user_service_api.get_user_by_id(user_id)

    await user_answer_repository.delete_answers_by_user(user_id)
    return f"all answers for user {user_id} deleted successfully"
