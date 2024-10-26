from fastapi import APIRouter

from app.db.add_diary_summary import add_diary_summary
from app.db.get_diary import get_diary_from_db, sort_diary_messages_timeorder
from app.schemas.diary_schema import Diary, FetchDiary
from app.utils.data_enum import DiaryField

diary_router = APIRouter()


@diary_router.post("/diary/summarize", response_model=Diary)
def fetch_diary(fetch_diary: FetchDiary) -> Diary:
    """指定された日付の日記から要約とフィードバックを生成してLINE botに返却"""
    add_diary_summary(
        fetch_diary.user_id, fetch_diary.year, fetch_diary.month, fetch_diary.day
    )

    # TODO: 何を返すかは用件等
    diary = Diary(
        year=fetch_diary.year,
        month=fetch_diary.month,
        day=fetch_diary.day,
        items=sorted_diary_items,
        summary=doc_dict.get(DiaryField.summary.value, None),
        feedback=doc_dict.get(DiaryField.feedback.value, None),
    )
    return diary
