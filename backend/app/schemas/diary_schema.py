from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TextItem(BaseModel):
    text: str
    timestamp: datetime


class FileItem(BaseModel):
    url: str
    mediatype: str
    timestamp: datetime


class Diary(BaseModel):
    year: int
    month: int
    day: int
    items: list[TextItem | FileItem]
    summary: Optional[str] = None
    feedback: Optional[str] = None


class FetchDiary(BaseModel):
    user_id: str
    year: int
    month: int
    day: int


class User(BaseModel):
    user_id: str
    display_name: str
    picture_url: str
    status_message: str
    created_at: datetime
    updated_at: datetime
    linkToken: str

    personality: str
    strength: str
    weakness: str


class FetchProfile(BaseModel):
    user_id: str
