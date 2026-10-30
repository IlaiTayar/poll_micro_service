from fastapi import APIRouter, HTTPException
from starlette import status

from model.base_model.answer_option import AnswerOption
from model.request_model.answer_option_request import AnswerOptionRequest
from service import answer_option_service

router:APIRouter = APIRouter(prefix="/answer_option", tags=["answer_option"])


def _exception_handler(result):
    if isinstance(result, HTTPException):
        raise result

    return result


@router.post("/creat", status_code=status.HTTP_201_CREATED)
async def create_option(option: AnswerOptionRequest) -> str:
    result = await answer_option_service.create_option(option)
    return _exception_handler(result)


@router.put("/update/{option_id}", status_code=status.HTTP_200_OK)
async def update_option_by_id(option_id: int, option: AnswerOptionRequest) -> str:
    result = await answer_option_service.update_option_by_id(option_id, option)
    return _exception_handler(result)


@router.get("/get/{option_id}", status_code=status.HTTP_200_OK)
async def get_option_by_id(option_id: int) -> AnswerOption:
    result = await answer_option_service.get_option_by_id(option_id)
    return _exception_handler(result)