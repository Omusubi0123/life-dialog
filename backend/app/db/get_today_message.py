from datetime import date

from sqlalchemy import select

from app.db.get_today_diary import get_or_create_diary
from app.db.model import Message
from app.utils.session_scope import get_session


def get_date_message(user_id: str, date: date) -> str:
    diary_id = get_or_create_diary(user_id, date)
    with get_session() as session:
        stmt = (
            select(Message)
            .where(Message.diary_id == diary_id)
            .order_by(Message.sent_at)
        )
        messages = session.execute(stmt).scalars().all()
        return messages
