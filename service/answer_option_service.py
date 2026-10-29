from exceptions.exception import answer_option_text_exists_exception, answer_option_not_found_exception
from model.request_model.answer_option_request import AnswerOptionRequest
from repository import answer_option_repository
from service import question_service


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










