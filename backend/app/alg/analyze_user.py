import json

from app.alg.format_diary_for_llm import (
    format_llm_response_json_to_str,
    format_messages_to_llm_input,
)
from app.alg.prompt.analyze_user_prompt import ANALYZE_USER_PROMPT
from app.alg.prompt.system_prompt import SYSTEM_PROMPT_JSON
from app.db.repositories.diary import DiaryRepository, MessageRepository
from app.db.session import session_scope
from app.utils.count_token import count_tokens
from app.utils.llm_response import openai_call


def analyze_user_by_llm(
    user_id: str,
    system_prompt: str = SYSTEM_PROMPT_JSON,
    summarize_diary_prompt: str = ANALYZE_USER_PROMPT,
    print_response: bool = True,
) -> tuple[str, str, str]:
    """ユーザーの全日記からユーザーの性格・強み・弱みをLLMで生成する

    Returns:
        LLMによるユーザーの性格・強み・弱み
    """
    with session_scope() as session:
        diary_repo = DiaryRepository(session)
        message_repo = MessageRepository(session)

        diary_list = diary_repo.get_user_diaries(user_id)
        print(f"Total diaries: {len(diary_list)}")

        diaries_str = ""
        # LLMのcontext lengthまで日記を追加。最新の日記から入れるために逆順で処理
        for diary in reversed(diary_list):
            messages = message_repo.get_by_user_and_date(user_id, diary.date)

            diary_str = format_llm_response_json_to_str(diary.title, diary.summary)
            # メッセージを辞書形式に変換してformat_messages_to_llm_inputに渡す
            messages_dict = [
                {
                    "media_type": msg.media_type,
                    "content": msg.content,
                    "sent_at": msg.sent_at,
                }
                for msg in messages
            ]
            diary_str += format_messages_to_llm_input(messages_dict, diary.date)
            diary_str += "\n\n"

            if len(diaries_str + diary_str) > 120000:
                break
            diaries_str = diary_str + diaries_str
            print(f"Current diary length: {count_tokens(diaries_str)} tokens")

    result = openai_call(
        system_prompt,
        summarize_diary_prompt.format(diaries=diaries_str),
        print_response=print_response,
        json_format=True,
    )

    result_dict = json.loads(result)

    personality = result_dict.get("personality", "")
    strength = result_dict.get("strength", "")
    weakness = result_dict.get("weakness", "")
    return personality, strength, weakness
