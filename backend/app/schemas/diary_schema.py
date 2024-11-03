from datetime import time
from typing import Optional

from pydantic import BaseModel


class MessageItem(BaseModel):
    media_type: str
    content: str
    time: time


class Diary(BaseModel):
    year: int
    month: int
    day: int
    items: list[MessageItem]
    title: Optional[str] = None
    summary: Optional[str] = None
    feedback: Optional[str] = None


class FetchDiary(BaseModel):
    user_id: str
    year: int
    month: int
    day: int


class DiaryVector(BaseModel):
    user_id: str
    diary_id: int
    diary_content: str
    diary_vector: list[float]
