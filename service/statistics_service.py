from typing import Optional, Union

from model.base_model.question import Question
from repository import statistics_repository as stats_repo
from service import question_service


async def get_question_option_statistics(question_id: int):
    question: Union[Question, Exception] = await question_service.get_question_by_id(question_id)
    if isinstance(question, Exception):
        return question

    return await stats_repo.get_question_option_counts(question_id)


async def get_question_total_statistics(question_id: int):
    question: Union[Question, Exception] = await question_service.get_question_by_id(question_id)
    if isinstance(question, Exception):
        return question

    return await stats_repo.get_question_total_answers(question_id)


async def get_user_answers_statistics(user_id: int):
    return await stats_repo.get_user_answers_summary(user_id)


async def get_user_total_answers_statistics(user_id: int):
    return await stats_repo.get_user_total_answers(user_id)


async def get_all_question_option_statistics(poll_id: Optional[int]):
    return await stats_repo.get_all_question_option_counts(poll_id)