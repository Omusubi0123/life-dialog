from enum import Enum


class QuickReplyField(Enum):
    """LINE botのクイックリプライ"""

    view_diary = "日記閲覧"
    interactive_mode = "対話モード"
    diary_mode = "日記モード"
    day_choice = "日付選択"


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
    display_name = "display_name"
    picture_url = "picture_url"
    status_message = "status_message"
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
