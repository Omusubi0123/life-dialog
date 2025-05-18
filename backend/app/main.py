from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.db.config import engine
from app.db.model import Base
from app.routes.diary import diary_router
from app.routes.line_bot import line_bot_router
from app.routes.user_profile import user_router
from app.scheduler import start_scheduler
from app.elastic.sync_diary import sync_diary_to_elasticsearch


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        start_scheduler()
        sync_diary_to_elasticsearch()
        yield
    except SQLAlchemyError as e:
        print(f"Database setup failed: {e}")
        raise HTTPException(status_code=500, detail="Database setup failed")


app = FastAPI(lifespan=lifespan)

app.include_router(diary_router)
app.include_router(user_router)
app.include_router(line_bot_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
