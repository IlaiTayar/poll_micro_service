from typing import Optional

from database import database

from model.base_model.poll import Poll
from model.request_model.poll_request import PollRequest

TABLE_NAME = "poll"


async def create_poll(poll: PollRequest) -> int:
    query = f"""
    INSERT INTO {TABLE_NAME} (poll_name)
    VALUES (:poll_name)
    """

    return await database.execute(query, values={"poll_name": poll.poll_name})


async def update_poll_by_id(poll_id: int, poll: PollRequest) -> int:
    query = f"""
    UPDATE {TABLE_NAME} SET poll_name = :poll_name
    WHERE poll_id = :poll_id
    """

    return await database.execute(query, values={"poll_id": poll_id, "poll_name": poll.poll_name})


async def get_poll_by_id(poll_id: int) -> Optional[Poll]:
    query = f"""
    SELECT * FROM {TABLE_NAME}
    WHERE poll_id = :poll_id
    """

    poll = await database.fetch_one(query, values={"poll_id": poll_id})

    return Poll(**dict(poll)) if poll else None


async def get_polls_by_name(poll_name: str) -> Optional[Poll]:
    query = f"""
    SELECT * FROM {TABLE_NAME} 
    WHERE poll_name = :poll_name
    """

    poll = await database.fetch_one(query, values={"poll_name": poll_name})

    return Poll(**dict(poll)) if poll else None


async def delete_poll_by_id(poll_id: int) -> str:
    query = f"""
    DELETE FROM {TABLE_NAME} WHERE poll_id = :poll_id
    """

    await database.execute(query, values={"poll_id": poll_id})
    return "poll deleted successfully"