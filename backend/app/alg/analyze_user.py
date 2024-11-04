import json

from app.alg.format_diary_for_llm import (
    format_llm_response_json_to_str,
    format_messages_to_llm_input,
)
from app.alg.prompt.analyze_user_prompt import ANALYZE_USER_PROMPT
from app.alg.prompt.system_prompt import SYSTEM_PROMPT_JSON
from app.db.get_diary import get_user_all_diary
from app.db.get_message import get_date_message
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
    diary_list = get_user_all_diary(user_id)
    messages_list = [get_date_message(user_id, diary["date"]) for diary in diary_list]

    diaries_str = ""
    for message, diary in zip(messages_list, diary_list):
        diaries_str += format_llm_response_json_to_str(
            diary.get("title"), diary.get("summary"), diary.get("feedback")
        )
        diaries_str += format_messages_to_llm_input(message, diary["date"])
        diaries_str += "\n\n"

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
