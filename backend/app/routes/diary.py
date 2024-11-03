from datetime import date

from fastapi import APIRouter

from app.db.get_diary import get_date_diary
from app.db.get_message import get_date_message
from app.schemas.diary_schema import Diary, FetchDiary, MessageItem
from app.utils.data_enum import DiaryField

diary_router = APIRouter()


@diary_router.post("/diary/fetch_diary", response_model=Diary)
def fetch_diary(fetch_diary: FetchDiary) -> Diary:
    """指定した日付のメッセージを時系列順に並び替えて返す"""
    view_date = date(fetch_diary.year, fetch_diary.month, fetch_diary.day)
    messages = get_date_message(fetch_diary.user_id, view_date)
    view_diary = get_date_diary(fetch_diary.user_id, view_date)

    # TODO: titleも追加, 日付の受け取り方・返し方
    if messages is None:
        diary = Diary(
            year=fetch_diary.year,
            month=fetch_diary.month,
            day=fetch_diary.day,
            items=[],
        )
    else:
        items = [
            MessageItem(
                media_type=message.get("media_type"),
                content=message.get("content"),
                time=message.get("sent_at"),
            )
            for message in messages
        ]

        diary = Diary(
            year=fetch_diary.year,
            month=fetch_diary.month,
            day=fetch_diary.day,
            items=items,
        )
        if view_diary:
            diary.title = (view_diary.get("title"),)
            diary.summary = (view_diary.get("summary"),)
            diary.feedback = (view_diary.get("feedback"),)
    return diary
