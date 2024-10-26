from fastapi import APIRouter

from app.db.get_diary import sort_diary_field_timeorder
from app.schemas.diary_schema import Diary, FetchDiary

diary_router = APIRouter()


@diary_router.post("/diary/fetch_diary", response_model=Diary)
def fetch_diary(fetch_diary: FetchDiary) -> Diary:
    sorted_diary_items = sort_diary_field_timeorder(
        fetch_diary.user_id, fetch_diary.year, fetch_diary.month, fetch_diary.day
    )
    diary = Diary(
        year=fetch_diary.year,
        month=fetch_diary.month,
        day=fetch_diary.day,
        items=sorted_diary_items,
    )
    return diary
