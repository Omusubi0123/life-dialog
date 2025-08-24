from app.alg.summarize_diary import summarize_diary_by_llm
from app.db.repositories.diary import DiaryRepository
from app.db.session import session_scope
from app.utils.get_japan_datetime import get_japan_date, get_japan_time


def set_diary_summary(user_id: str, diary_id: int) -> tuple[str, str, str]:
    """日記の要約を生成し、DBに保存する"""
    title, summary, feedback = summarize_diary_by_llm(user_id, get_japan_date())
    with session_scope() as session:
        diary_repo = DiaryRepository(session)
        diary_repo.update_summary(diary_id, title, summary, feedback)
    print(f"Diary summary updated!! Time:", get_japan_time(), flush=True)
    return title, summary, feedback
