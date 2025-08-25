from datetime import date

from app.alg.format_diary_for_llm import (
    format_llm_response_json_to_str,
    format_messages_to_llm_input,
)
from app.db.repositories.diary import (
    DiaryRepository,
    DiaryVectorRepository,
    MessageRepository,
)
from app.db.session import session_scope
from app.utils.get_japan_datetime import get_japan_time
from app.utils.llm_response import get_embedding


def set_diary_vector(user_id: str, target_date: date) -> dict:
    """指定した日の日記のベクトルを設定する

    Args:
        user_id (str): LINEユーザーID
        target_date (date): 日付
    """
    with session_scope() as session:
        diary_repo = DiaryRepository(session)
        message_repo = MessageRepository(session)
        vector_repo = DiaryVectorRepository(session)

        diary = diary_repo.get_by_user_and_date(user_id, target_date)
        messages = message_repo.get_by_user_and_date(user_id, target_date)

        if not diary:
            return None

        summary_str = format_llm_response_json_to_str(
            diary.title, diary.summary,
        )
        diary_str = format_messages_to_llm_input(
            [
                {
                    "media_type": msg.media_type,
                    "content": msg.content,
                    "sent_at": msg.sent_at,
                }
                for msg in messages
            ],
            target_date,
        )

        content = f"{summary_str}\n{diary_str}"
        vector = get_embedding(content)

        new_diary_vector = vector_repo.upsert(
            user_id, diary.diary_id, diary.date, content, vector
        )
        print(f"Diary vector added!! Time:", get_japan_time(), flush=True)
        return new_diary_vector.to_dict()
