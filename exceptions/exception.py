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


def poll_has_questions(poll_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Poll with id {poll_id} has questions"
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


def question_has_options(question_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Question with id {question_id} has options"
    )


def question_already_answered(question_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Question with id {question_id} has answers"
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


def option_already_chosen_exception(user_id: int, question_id: int, option_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"User {user_id} already chose option {option_id} for question {question_id}"
    )


def question_answers_exist_exception(question_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Cannot update options for question {question_id} because user answers already exist"
    )