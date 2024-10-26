from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class QuickReplyField(Enum):
    """LINE botのクイックリプライ"""

    view_diary = "今日の日記を見る"
    interactive_mode = "人生と対話する"
    diary_mode = "人生を記録する"
    day_choice = "日付選択"


class RootCollection(Enum):
    user = "Users"
    diary = "Diary"


class DiaryCollection(Enum):
    diary = "diary"


class DiaryField(Enum):
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
