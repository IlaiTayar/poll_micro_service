from typing import Optional

from fastapi import APIRouter, HTTPException
from starlette import status

from model.base_model.statistics import (
    QuestionOptionStat,
    QuestionResultsEntry,
    QuestionTotalStat,
    UserAnswerSummary,
    UserTotalAnsweredStat,
)
from service import statistics_service as stats_service


router: APIRouter = APIRouter(prefix="/statistics", tags=["statistics"])


def _exception_handler(result):
    if isinstance(result, HTTPException):
        raise result
    return result


@router.get("/question/{question_id}/options", response_model=list[QuestionOptionStat], status_code=status.HTTP_200_OK)
async def get_question_option_statistics(question_id: int):
    result = await stats_service.get_question_option_statistics(question_id)
    return _exception_handler(result)


@router.get("/question/{question_id}/total", response_model=QuestionTotalStat, status_code=status.HTTP_200_OK)
async def get_question_total_statistics(question_id: int):
    result = await stats_service.get_question_total_statistics(question_id)
    return _exception_handler(result)


@router.get("/user/{user_id}/answers", response_model=UserAnswerSummary, status_code=status.HTTP_200_OK)
async def get_user_answers_statistics(user_id: int):
    result = await stats_service.get_user_answers_statistics(user_id)
    return _exception_handler(result)


@router.get("/user/{user_id}/total", response_model=UserTotalAnsweredStat, status_code=status.HTTP_200_OK)
async def get_user_total_answers_statistics(user_id: int):
    result = await stats_service.get_user_total_answers_statistics(user_id)
    return _exception_handler(result)


@router.get("/questions/results", response_model=list[QuestionResultsEntry], status_code=status.HTTP_200_OK)
async def get_all_question_option_statistics(poll_id: Optional[int] = None):
    result = await stats_service.get_all_question_option_statistics(poll_id)
    return _exception_handler(result)
