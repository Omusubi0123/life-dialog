from sqlalchemy import update

from app.alg.summarize_diary import summarize_diary_by_llm
from app.db.model import Diary
from app.utils.get_japan_datetime import get_japan_date
from app.utils.session_scope import get_session


def set_diary_summary(user_id: str, diary_id: int) -> tuple[str, str, str]:
    """日記の要約を生成し、DBに保存する"""
    title, summary, feedback = summarize_diary_by_llm(user_id, get_japan_date())
    with get_session() as session:
        stmt = (
            update(Diary)
            .where(Diary.diary_id == diary_id)
            .values(title=title, summary=summary, feedback=feedback)
        )
        session.execute(stmt)
    return title, summary, feedback
