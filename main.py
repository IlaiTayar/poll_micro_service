from fastapi import FastAPI

from controller.answer_option_controller import router as option_router
from controller.poll_controller import router as poll_router
from controller.question_controller import router as question_router
from database import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


app.include_router(poll_router)
app.include_router(question_router)
app.include_router(option_router)
