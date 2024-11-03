from datetime import date

from app.alg.format_diary_for_llm import (
    format_llm_response_json_to_str,
    format_messages_to_llm_input,
)
from app.db.db_insert import add_diary_vector
from app.db.get_diary import get_date_diary
from app.db.get_message import get_date_message
from app.utils.llm_response import get_embedding
from app.utils.session_scope import get_session


def set_diary_vector(user_id: str, date: date) -> dict:
    """指定した日の日記のベクトルを設定する

    Args:
        user_id (str): LINEユーザーID
        date (date): 日付
    """
    with get_session() as session:
        diary = get_date_diary(user_id, date)
        messages = get_date_message(user_id, date)

        summary_str = format_llm_response_json_to_str(
            diary.get("title"), diary.get("summary"), diary.get("feedback")
        )
        diary_str = format_messages_to_llm_input(messages, date)

        content = f"{summary_str}\n{diary_str}"
        vector = get_embedding(content)

        new_diary_vector = add_diary_vector(
            session, user_id, diary.get("diary_id"), content, vector
        )
        return new_diary_vector.to_dict()
