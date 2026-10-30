from fastapi import HTTPException, APIRouter
from starlette import status

from model.base_model.user_answer import UserAnswer
from model.request_model.user_answer_request import UserAnswerRequest
from service import user_answer_service

router: APIRouter = APIRouter(prefix="user_answer", tags=["user_answer"])


def _exception_handler(result):
    if isinstance(result, HTTPException):
        raise result

    return result


@router.post("/creat", status_code=status.HTTP_201_CREATED)
async def create_answer(answer: UserAnswerRequest) -> str:
    result = await user_answer_service.create_answer(answer)
    return _exception_handler(result)


@router.put("/update/{answer_id}", status_code=status.HTTP_200_OK)
async def update_answer_by_id(answer_id: int, answer: UserAnswerRequest) -> str:
    result = await user_answer_service.update_answer_by_id(answer_id, answer)
    return _exception_handler(result)


@router.get("/get/{answer_id}", status_code=status.HTTP_200_OK)
async def get_answer_by_id(answer_id: int) -> UserAnswer:
    result = await user_answer_service.get_answer_by_id(answer_id)
    return _exception_handler(result)


@router.delete("/delete/{answer_id}", status_code=status.HTTP_200_OK)
async def delete_answer_by_id(answer_id: int) -> str:
    result = await user_answer_service.delete_answer_by_id(answer_id)
    return _exception_handler(result)