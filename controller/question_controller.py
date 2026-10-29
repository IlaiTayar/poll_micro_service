from fastapi import APIRouter, HTTPException
from starlette import status

from model.base_model.question import Question
from model.request_model.question_request import QuestionRequest
from service import question_service

router: APIRouter = APIRouter(prefix="/question", tags=["question"])


def _exception_handler(result):
    if isinstance(result, HTTPException):
        raise result

    return result


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_question(question: QuestionRequest) -> str:
    result = await question_service.create_question(question)
    return _exception_handler(result)


@router.put("/update/{question_id}", status_code=status.HTTP_200_OK)
async def update_question_by_id(question_id: int, question: QuestionRequest) -> str:
    result = await question_service.update_question_by_id(question_id, question)
    return _exception_handler(result)


@router.get("/get/{question_id}", status_code=status.HTTP_200_OK)
async def get_question_by_id(question_id: int) -> Question:
    result = await question_service.get_question_by_id(question_id)
    return _exception_handler(result)