from datetime import date

from sqlalchemy import select

from app.db.db_insert import add_diary
from app.db.model import Diary
from app.utils.session_scope import get_session


def get_or_create_diary_id(user_id: str, date: date) -> int:
    """指定した日のユーザーの日記を取得または作成し、日記IDを返す"""
    with get_session() as session:
        stmt = select(Diary).where(Diary.user_id == user_id, Diary.date == date)
        existing_diary = session.scalar(stmt)

        if existing_diary:
            return existing_diary.diary_id

        new_diary = add_diary(
            session,
            user_id=user_id,
            date=date,
        )

        return new_diary.diary_id


def get_date_diary(user_id: str, date: date) -> dict:
    """指定したユーザー・日付の日記を取得"""
    with get_session() as session:
        stmt = select(Diary).where(Diary.user_id == user_id, Diary.date == date)
        diary = session.scalar(stmt)
        return diary.to_dict() if diary else None


def get_user_all_diary(user_id: str) -> list[dict]:
    """指定したユーザーの全日記を時系列順にして取得"""
    with get_session() as session:
        stmt = select(Diary).where(Diary.user_id == user_id).order_by(Diary.date)
        diaries = session.execute(stmt).scalars().all()
        return [diary.to_dict() for diary in diaries]
