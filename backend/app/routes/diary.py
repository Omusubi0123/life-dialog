from fastapi import APIRouter

from app.db.get_diary import get_diary_from_db
from app.db.sort_diary_messages import sort_diary_messages_timeorder
from app.schemas.diary_schema import Diary, FetchDiary
from app.utils.data_enum import DiaryField

diary_router = APIRouter()


@diary_router.post("/diary/fetch_diary", response_model=Diary)
def fetch_diary(fetch_diary: FetchDiary) -> Diary:
    """日記を取得しメッセージを時系列順に並び替えて返す"""
    doc_dict = get_diary_from_db(
        fetch_diary.user_id, fetch_diary.year, fetch_diary.month, fetch_diary.day
    )

    if doc_dict is None:
        diary = Diary(
            year=fetch_diary.year,
            month=fetch_diary.month,
            day=fetch_diary.day,
            items=[],
            summary="",
            feedback="",
        )
    else:    
        sorted_diary_items = sort_diary_messages_timeorder(doc_dict)
        diary = Diary(
            year=fetch_diary.year,
            month=fetch_diary.month,
            day=fetch_diary.day,
            items=sorted_diary_items,
            summary=doc_dict.get(DiaryField.summary.value),
            feedback=doc_dict.get(DiaryField.feedback.value),
        )
    return diary
