from datetime import datetime

from pydantic import BaseModel


class UserProfile(BaseModel):
    user_id: str
    name: str
    created_at: datetime
    updated_at: datetime
    mode: str
    icon_url: str
    status_message: str
    link_token: str

    personality: str | None = None
    strength: str | None = None
    weakness: str | None = None


class FetchProfile(BaseModel):
    user_id: str
