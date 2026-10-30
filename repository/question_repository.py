from typing import Optional, List

from database import database
from model.base_model.question import Question
from model.request_model.question_request import QuestionRequest

TABLE_NAME = "question"


async def create_question(question: QuestionRequest) -> int:
    query = f"""
    INSERT INTO {TABLE_NAME} (poll_id, question_text)
    VALUES (:poll_id, :question_text)
    """

    values = {"poll_id": question.poll_id,
              "question_text": question.question_text}

    return await database.execute(query, values)


async def update_question_by_id(question_id, question: QuestionRequest) -> int:
    query = f"""
    UPDATE {TABLE_NAME} SET poll_id = :poll_id, question_text = :question_text
    WHERE question_id = :question_id
    """

    values = {"question_id": question_id,
              "poll_id": question.poll_id,
              "question_text": question.question_text}

    return await database.execute(query, values)


async def get_question_by_id(question_id: int) -> Optional[Question]:
    query = f"""
    SELECT * FROM {TABLE_NAME} 
    WHERE question_id = :question_id
    """

    question = await database.fetch_one(query, values={"question_id": question_id})

    return Question(**dict(question)) if question else None


async def get_questions_by_text(question_text: str) -> List[Question]:
    query = f"""
    SELECT * FROM {TABLE_NAME} 
    WHERE question_text = :question_text
    """

    questions = await database.fetch_all(query, values={"question_text": question_text})
    return [Question(**dict(question)) for question in questions]


async def get_questions_by_poll(poll_id: int) -> List[Question]:
    query = f"""
    SELECT * FROM {TABLE_NAME} 
    WHERE poll_id = :poll_id
    """

    questions = await database.fetch_all(query, values={"poll_id": poll_id})
    return [Question(**dict(question)) for question in questions]


async def delete_question_by_id(question_id: int) -> str:
    query = f"""
    DELETE FROM {TABLE_NAME} 
    WHERE question_id = :question_id
    """

    await database.execute(query, values={"question_id": question_id})

    return "question deleted successfully"

















