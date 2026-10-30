from exceptions.exception import answer_option_text_exists_exception, answer_option_not_found_exception, \
    question_answers_exist_exception
from model.request_model.answer_option_request import AnswerOptionRequest
from repository import answer_option_repository
from service import question_service, user_answer_service


async def create_option(option: AnswerOptionRequest):
    existing_question = await question_service.get_question_by_id(option.question_id)
    if isinstance(existing_question, Exception):
        return existing_question

    existing_text = await get_options_by_text(option.option_text)
    for text in existing_text:
        if option.question_id == text.question_id:
            return answer_option_text_exists_exception(option.question_id, option.option_text)

    new_option_id = await answer_option_repository.create_option(option)
    return f"new option created with id: {new_option_id} for answer: {option.question_id}"


async def update_option_by_id(option_id: int, option: AnswerOptionRequest):
    existing_option = await get_option_by_id(option_id)
    if isinstance(existing_option, Exception):
        return existing_option

    existing_question = await question_service.get_question_by_id(option.question_id)
    if isinstance(existing_question, Exception):
        return existing_question

    existing_text = await get_options_by_text(option.option_text)
    for text in existing_text:
        if option.question_id == text.question_id:
            return answer_option_text_exists_exception(option.question_id, option.option_text)

    already_answered = await user_answer_service.get_answers_by_question(option.question_id)
    if already_answered:
        return question_answers_exist_exception(option.question_id)

    await answer_option_repository.update_option_by_id(option_id, option)
    return f"option updated with id: {option_id} for answer: {option.question_id}"


async def get_option_by_id(option_id: int):
    option = await answer_option_repository.get_option_by_id(option_id)
    if option is None:
        return answer_option_not_found_exception(option_id)

    return option


async def get_options_by_text(text: str):
    options = await answer_option_repository.get_options_by_text(text)

    return options


async def delete_option_by_id(option_id: int):
    existing_option = await get_option_by_id(option_id)
    if isinstance(existing_option, Exception):
        return existing_option

    already_answered = await user_answer_service.get_answers_by_option(option_id)
    if isinstance(already_answered, Exception):
        return already_answered

    await answer_option_repository.delete_option_by_id(option_id)
    return f"option deleted with id: {option_id}"







