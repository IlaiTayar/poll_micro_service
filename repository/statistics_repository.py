from typing import Optional

from database import database
from model.base_model.statistics import (
    QuestionOptionStat,
    QuestionResultsEntry,
    QuestionTotalStat,
    UserAnswerSummary,
    UserAnswerSummaryEntry,
    UserTotalAnsweredStat,
)


async def get_question_option_counts(question_id: int):
    query = """
    SELECT
        answer_option.question_id AS question_id,
        answer_option.option_id AS option_id,
        answer_option.option_text AS option_text,
        COUNT(DISTINCT user_answer.user_id) AS count
    FROM answer_option
    LEFT JOIN user_answer
        ON user_answer.question_id = answer_option.question_id
       AND user_answer.option_id = answer_option.option_id
    WHERE answer_option.question_id = :question_id
    GROUP BY answer_option.question_id, answer_option.option_id, answer_option.option_text
    ORDER BY answer_option.option_id
    """

    rows = await database.fetch_all(query, values={"question_id": question_id})
    return [QuestionOptionStat(**dict(row)) for row in rows]


async def get_question_total_answers(question_id: int):
    query = """
    SELECT
        user_answer.question_id AS question_id,
        COUNT(DISTINCT user_answer.user_id) AS total_users_answered
    FROM user_answer
    WHERE user_answer.question_id = :question_id
    GROUP BY user_answer.question_id
    """

    row = await database.fetch_one(query, values={"question_id": question_id})
    if row is None:
        return QuestionTotalStat(question_id=question_id, total_users_answered=0)

    return QuestionTotalStat(**dict(row))


async def get_user_answers_summary(user_id: int):
    query = """
    SELECT
        user_answer.answer_id AS answer_id,
        user_answer.user_id AS user_id,
        user_answer.question_id AS question_id,
        question.question_text AS question_text,
        user_answer.option_id AS option_id,
        answer_option.option_text AS option_text
    FROM user_answer
    LEFT JOIN question
        ON question.question_id = user_answer.question_id
    LEFT JOIN answer_option
        ON answer_option.option_id = user_answer.option_id
    WHERE user_answer.user_id = :user_id
    ORDER BY user_answer.question_id, user_answer.answer_id
    """

    rows = await database.fetch_all(query, values={"user_id": user_id})
    answer_rows = [UserAnswerSummaryEntry(**dict(row)) for row in rows]

    question_answer = {}
    for item in answer_rows:
        question_answer[item.answer_id] = {
            "user_id": item.user_id,
            "answer_id": item.answer_id,
            "question_id": item.question_id,
            "question_text": item.question_text,
            "option_id": item.option_id,
            "option_text": item.option_text,
        }

    return UserAnswerSummary(user_id=user_id, question_answer=question_answer)


async def get_user_total_answers(user_id: int):
    query = """
    SELECT COUNT(DISTINCT user_answer.question_id) AS total_questions_answered
    FROM user_answer
    WHERE user_answer.user_id = :user_id
    """

    row = await database.fetch_one(query, values={"user_id": user_id})
    if row is None:
        return UserTotalAnsweredStat(user_id=user_id, total_questions_answered=0)

    return UserTotalAnsweredStat(**dict(row))


async def get_all_question_option_counts(poll_id: Optional[int]):
    query = """
    SELECT
        question.poll_id AS poll_id,
        question.question_id AS question_id,
        question.question_text AS question_text,
        answer_option.option_id AS option_id,
        answer_option.option_text AS option_text,
        COUNT(DISTINCT user_answer.user_id) AS count
    FROM question
    LEFT JOIN answer_option
        ON answer_option.question_id = question.question_id
    LEFT JOIN user_answer
        ON user_answer.question_id = question.question_id
       AND user_answer.option_id = answer_option.option_id
    WHERE (:poll_id IS NULL OR question.poll_id = :poll_id)
    GROUP BY
        question.poll_id,
        question.question_id,
        question.question_text,
        answer_option.option_id,
        answer_option.option_text
    ORDER BY question.poll_id, question.question_id, answer_option.option_id
    """

    rows = await database.fetch_all(query, values={"poll_id": poll_id})
    return [QuestionResultsEntry(**dict(row)) for row in rows]
