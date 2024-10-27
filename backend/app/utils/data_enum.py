from enum import Enum


class QuickReplyField(Enum):
    """LINE botのクイックリプライ"""

    view_diary = "今日の日記"
    interactive_mode = "対話する"
    diary_mode = "記録する"
    day_choice = "日付選択"

    @classmethod
    def get_values(cls):
        return [item.value for item in cls]

    @classmethod
    def get_keys(cls):
        return [item.name for item in cls]


class AnalyzeUserField(Enum):
    """LLMが分析したユーザーの情報"""

    personality = "personality"
    strength = "strength"
    weakness = "weakness"


class RootCollection(Enum):
    """DBのルートコレクション"""

    user = "Users"
    diary = "Diary"


class UserField(Enum):
    """DBのユーザードキュメントフィールド"""

    user_id = "user_id"

    user_name = "user_name"
    icon_url = "icon_url"
    status_message = "status_message"

    status = "status"
    created_at = "created_at"
    updated_at = "updated_at"
    linkToken = "linkToken"

    personality = "personality"
    strength = "strength"
    weakness = "weakness"


class DiaryCollection(Enum):
    """DBの日記コレクション"""

    diary = "diary"


class DiaryField(Enum):
    """DBの日記ドキュメントフィールド"""

    diary_id = "diary_id"
    date = "date"
    summary = "summary"
    feedback = "feedback"
    texts = "texts"
    files = "files"


class TextField(Enum):
    """DBの日記ドキュメントのテキストフィールド"""

    key = "text{}"
    text = "text"
    timestamp = "timestamp"


class FileField(Enum):
    """DBの日記ドキュメントのファイルフィールド"""

    key = "file{}"
    url = "url"
    mediatype = "mediatype"
    timestamp = "timestamp"
