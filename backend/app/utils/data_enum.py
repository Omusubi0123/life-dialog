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


class DiaryField(Enum):
    """DBの日記ドキュメントフィールド"""

    diary_id = "diary_id"
    date = "date"
    title = "title"
    content = "content"
    summary = "summary"
    feedback = "feedback"
    texts = "texts"
    files = "files"
