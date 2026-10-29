from fastapi import HTTPException
from starlette import status


def poll_not_found_exception(poll_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Poll with id {poll_id} was not found"
    )


def poll_name_exists_exception(poll_name: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Poll with name '{poll_name}' already exists"
    )


def question_not_found_exception(question_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Question with id {question_id} was not found"
    )


def question_already_exists_exception(poll_id: int, question_text: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Question '{question_text}' already exists in poll {poll_id}"
    )


def answer_option_not_found_exception(option_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Answer option with id {option_id} was not found"
    )


def answer_option_text_exists_exception(question_id: int, option_text: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Answer option '{option_text}' already exists for question {question_id}"
    )


def answer_not_found_exception(answer_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Answer with id {answer_id} was not found"
    )


def answer_already_exists_exception(user_id: int, question_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"User {user_id} already answered question {question_id}"
    )


def user_not_registered_exception(user_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"User with id {user_id} is not registered"
    )


def cannot_update_answer_user_id_exception(answer_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Cannot update user_id for answer {answer_id}"
    )