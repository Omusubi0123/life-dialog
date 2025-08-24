import json
from datetime import date

from app.alg.format_diary_for_llm import format_messages_to_llm_input
from app.alg.prompt.summarize_diary_prompt import SUMMARIZE_DIARY_PROMPT
from app.alg.prompt.system_prompt import SYSTEM_PROMPT_JSON
from app.db.repositories.diary import MessageRepository
from app.db.session import session_scope
from app.utils.data_enum import DiaryField
from app.utils.llm_response import openai_call


def summarize_diary_by_llm(
    user_id: str,
    date: date,
    system_prompt: str = SYSTEM_PROMPT_JSON,
    summarize_diary_prompt: str = SUMMARIZE_DIARY_PROMPT,
    print_response: bool = True,
) -> tuple[str, str, str, str]:
    """日記から1日の出来事の要約をLLMで生成する

    Returns:
        LLMによる日記の要約
    """
    with session_scope() as session:
        message_repo = MessageRepository(session)
        messages = message_repo.get_by_user_and_date(user_id, date)

        # メッセージを辞書形式に変換してformat_messages_to_llm_inputに渡す
        messages_dict = [
            {
                "media_type": msg.media_type,
                "content": msg.content,
                "sent_at": msg.sent_at,
            }
            for msg in messages
        ]
        diary_str = format_messages_to_llm_input(messages_dict, date)

    result = openai_call(
        system_prompt,
        summarize_diary_prompt.format(diary=diary_str),
        print_response=print_response,
        json_format=True,
    )

    result_dict = json.loads(result)

    title = result_dict.get(DiaryField.title.value, "")
    summary = result_dict.get(DiaryField.summary.value, "")
    feedback = result_dict.get(DiaryField.feedback.value, "")
    return title, summary, feedback
