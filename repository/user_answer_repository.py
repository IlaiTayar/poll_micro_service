from typing import Optional, List

from database import database
from model.base_model.user_answer import UserAnswer
from model.request_model.user_answer_request import UserAnswerRequest

TABLE_NAME = "user_answer"


async def create_answer(answer: UserAnswerRequest) -> int:
    query = f"""
    INSERT INTO {TABLE_NAME} (user_id, question_id, option_id)
    VALUES (:user_id, :question_id, :option_id)
    """

    values = {"user_id": answer.user_id,
              "question_id": answer.question_id,
              "option_id": answer.option_id}

    return await database.execute(query, values)


async def update_answer_by_id(answer_id: int, answer: UserAnswerRequest) -> int:
    query = f"""
    UPDATE {TABLE_NAME} SET user_id = :user_id, question_id = :question_id, option_id = :option_id
    WHERE answer_id = :answer_id
    """

    values = {"answer_id": answer_id,
              "user_id": answer.user_id,
              "question_id": answer.question_id,
              "option_id": answer.option_id}

    return await database.execute(query, values)


async def get_answer_by_id(answer_id: int) -> Optional[UserAnswer]:
    query = f"""
    SELECT * FROM {TABLE_NAME} 
    WHERE answer_id = :answer_id
    """

    user_answer = await database.fetch_one(query, values={"answer_id": answer_id})

    return UserAnswer(**dict(user_answer)) if user_answer else None


async def get_answers_by_user(user_id: int) -> List[UserAnswer]:
    query = f"""
    SELECT * FROM {TABLE_NAME} 
    WHERE user_id = :user_id
    """

    user_answers = await database.fetch_all(query, values={"user_id": user_id})
    return [UserAnswer(**dict(user_answer)) for user_answer in user_answers]


async def get_answers_by_option(option_id: int) -> List[UserAnswer]:
    query = f"""
    SELECT * FROM {TABLE_NAME} 
    WHERE option_id = :option_id
    """

    option_answers = await database.fetch_all(query, values={"option_id": option_id})
    return [UserAnswer(**dict(option_answer)) for option_answer in option_answers]


async def get_answers_by_question(question_id: int) -> List[UserAnswer]:
    query = f"""
    SELECT * FROM {TABLE_NAME} 
    WHERE question_id = :question_id
    """

    user_answers = await database.fetch_all(query, values={"question_id": question_id})
    return [UserAnswer(**dict(user_answer)) for user_answer in user_answers]


async def delete_answer_by_id(answer_id: int) -> str:
    query = f"""
    DELETE FROM {TABLE_NAME} 
    WHERE answer_id = :answer_id
    """

    await database.execute(query, values={"answer_id": answer_id})

    return "question deleted successfully"