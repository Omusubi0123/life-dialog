from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    user_name: str
    icon_url: str
    status_message: str
    created_at: datetime
    updated_at: datetime
    linkToken: str

    personality: str
    strength: str
    weakness: str


class FetchProfile(BaseModel):
    user_id: str
