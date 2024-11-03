from datetime import date

from sqlalchemy import select

from app.db.db_insert import add_diary
from app.db.model import Diary
from app.utils.session_scope import get_session


def get_or_create_today_diary(user_id: str) -> int:
    """ユーザーの今日の日記を取得または作成し、日記IDを返す"""
    today = date.today()

    with get_session() as session:
        # user_id と date が一致するデータを検索
        stmt = select(Diary).where(Diary.user_id == user_id, Diary.date == today)
        existing_diary = session.scalar(stmt)

        if existing_diary:
            return existing_diary.diary_id

        new_diary = add_diary(
            session,
            user_id=user_id,
            date=today,
        )

        return new_diary.diary_id
