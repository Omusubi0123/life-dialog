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


class DiaryCollection(Enum):
    diary = "diary"


class DiaryField(Enum):
    date = "date"
    summary = "summary"
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
