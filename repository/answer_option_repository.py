from typing import Optional, List

from database import database
from model.base_model.answer_option import AnswerOption
from model.request_model.answer_option_request import AnswerOptionRequest

TABLE_NAME = "answer_option"


async def create_option(option: AnswerOptionRequest) -> int:
    query = f"""
    INSERT INTO {TABLE_NAME} (question_id, option_text)
    VALUES (:question_id, :option_text)
    """

    values = {"question_id": option.question_id,
              "option_text": option.option_text}

    return await database.execute(query, values)


async def update_option_by_id(option_id: int, option: AnswerOptionRequest) -> int:
    query = f"""
    UPDATE {TABLE_NAME} SET question_id = :question_id, option_text = :option_text
    WHERE option_id = :option_id
    """

    values = {"option_id": option_id,
              "question_id": option.question_id,
              "option_text": option.option_text}

    return await database.execute(query, values)


async def get_option_by_id(option_id: int) -> Optional[AnswerOption]:
    query = f"""
    SELECT * FROM {TABLE_NAME} 
    WHERE option_id = :option_id
    """

    answer_option = await database.fetch_one(query, values={"option_id": option_id})

    return AnswerOption(**dict(answer_option)) if answer_option else None


async def get_options_by_text(option_text: str) -> List[AnswerOption]:
    query = f"""
    SELECT * FROM {TABLE_NAME} 
    WHERE option_text = :option_text
    """

    options = await database.fetch_all(query, values={"option_text": option_text})
    return [AnswerOption(**dict(option)) for option in options]


async def delete_option_by_id(option_id: int) -> str:
    query = f"""
    DELETE FROM {TABLE_NAME} 
    WHERE option_id = :option_id
    """

    await database.execute(query, values={"option_id": option_id})

    return "option deleted successfully"
