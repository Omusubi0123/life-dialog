from fastapi import FastAPI

from app.routes.diary import diary_router
from app.routes.line_bot import line_bot_router

app = FastAPI()

app.include_router(line_bot_router)
app.include_router(diary_router)
