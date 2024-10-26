from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class QuickReplyField(Enum):
    """LINE botのクイックリプライ"""

    view_diary = "日記閲覧"
    interactive_mode = "対話モード"
    diary_mode = "日記モード"
    day_choice = "日付選択"


class RootCollection(Enum):
    user = "Users"
    diary = "Diary"


class UserField(Enum):
    user_id = "user_id"
    display_name = "display_name"
    picture_url = "picture_url"
    status_message = "status_message"
    created_at = "created_at"
    updated_at = "updated_at"
    linkToken = "linkToken"


class DiaryCollection(Enum):
    diary = "diary"


class DiaryField(Enum):
    diary_id = "diary_id"
    date = "date"
    summary = "summary"
    feedback = "feedback"
    texts = "texts"
    files = "files"


class TextField(Enum):
    key = "text{}"
    text = "text"
    timestamp = "timestamp"


class FileField(Enum):
    key = "file{}"
    url = "url"
    mediatype = "mediatype"
    timestamp = "timestamp"
