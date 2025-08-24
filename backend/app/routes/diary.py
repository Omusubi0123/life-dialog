from datetime import date

from fastapi import APIRouter, Depends

from app.db.repositories.diary import DiaryRepository, MessageRepository
from app.db.session import session_scope
from app.db.set_diary_vector import set_diary_vector
from app.schemas.diary_schema import Diary, DiaryVector, FetchDiary, MessageItem
from app.utils.auth import AuthenticatedUser, get_current_user_with_line_id

diary_router = APIRouter()


@diary_router.post("/diary/fetch_diary", response_model=Diary)
def fetch_diary(
    fetch_diary: FetchDiary,
    current_user: AuthenticatedUser = Depends(get_current_user_with_line_id),
) -> Diary:
    """指定した日付のメッセージを時系列順に並び替えて返す（認証必須）"""
    # 認証されたユーザーのLINE IDを使用
    user_id = current_user.line_user_id
    view_date = date(fetch_diary.year, fetch_diary.month, fetch_diary.day)

    with session_scope() as session:
        message_repo = MessageRepository(session)
        diary_repo = DiaryRepository(session)

        messages = message_repo.get_by_user_and_date(user_id, view_date)
        view_diary = diary_repo.get_by_user_and_date(user_id, view_date)

        # TODO: 日付の受け取り方・返し方
        if not messages:
            diary = Diary(
                year=fetch_diary.year,
                month=fetch_diary.month,
                day=fetch_diary.day,
                items=[],
            )
        else:
            items = [
                MessageItem(
                    media_type=message.media_type,
                    content=message.content,
                    time=message.sent_at,
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
                diary.title = (view_diary.title,)
                diary.summary = (view_diary.summary,)
                diary.feedback = (view_diary.feedback,)
        return diary


@diary_router.post("/diary/register_vector", response_model=DiaryVector)
def register_vector(
    register_diary: FetchDiary,
    current_user: AuthenticatedUser = Depends(get_current_user_with_line_id),
) -> DiaryVector:
    """日記のベクトルを登録・既に存在する場合は更新する（認証必須）"""
    # 認証されたユーザーのLINE IDを使用
    user_id = current_user.line_user_id
    register_date = date(register_diary.year, register_diary.month, register_diary.day)
    vector = set_diary_vector(user_id, register_date)
    diary_vector = DiaryVector(**vector)
    return diary_vector
