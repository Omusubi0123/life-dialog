from datetime import date

from sqlalchemy import select

from app.db.get_diary import get_or_create_diary_id
from app.db.session import session_scope
from app.models.diary import Message


def get_date_message(user_id: str, date: date) -> list[dict]:
    """指定したユーザー・日付のメッセージをすべて取得

    Args:
        user_id (str): LINEユーザーID
        date (date): 日付

    Returns:
        list[Message]: 指定したユーザー・日付のメッセージ
    """
    diary_id = get_or_create_diary_id(user_id, date)
    with session_scope() as session:
        stmt = (
            select(Message)
            .where(Message.diary_id == diary_id)
            .order_by(Message.sent_at)
        )
        messages = session.execute(stmt).scalars().all()
        return [message.to_dict() for message in messages]
