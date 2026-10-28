from typing import Union

from fastapi import APIRouter, HTTPException
from starlette import status

from model.base_model.poll import PollError
from model.base_model.question import QuestionError, Question
from model.request_model.question_request import QuestionRequest
from service import question_service

router: APIRouter = APIRouter(prefix="/question",
                              tags=["question"])


def _exception_handler(result):
    if isinstance(result, QuestionError) or isinstance(result, PollError):

        if result == QuestionError.QUESTION_NOT_FOUND:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.value)

        if result == QuestionError.QUESTION_ALREADY_EXISTS:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=result.value)

        if result == PollError.NOT_FOUND:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.value)

    return result


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_question(question: QuestionRequest) -> str:
    result: Union[str, QuestionError, PollError] = await question_service.create_question(question)

    return _exception_handler(result)


@router.put("/update/{question_id}", status_code=status.HTTP_200_OK)
async def update_question_by_id(question_id: int, question: QuestionRequest) -> str:
    result: Union[str, QuestionError] = await question_service.update_question_by_id(question_id, question)

    return _exception_handler(result)


@router.get("/get/{question_id}", status_code=status.HTTP_200_OK)
async def get_question_by_id(question_id: int) -> Question:
    result: Union[Question, QuestionError] = await question_service.get_question_by_id(question_id)

    return _exception_handler(result)