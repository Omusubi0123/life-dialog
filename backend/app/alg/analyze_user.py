import json

from app.alg.format_diary_for_llm import (
    format_llm_response_json_to_str,
    format_sorted_diary_to_llm_input,
)
from app.alg.prompt.analyze_user_prompt import ANALYZE_USER_PROMPT
from app.alg.prompt.system_prompt import SYSTEM_PROMPT_JSON
from app.db.get_diary import get_all_diary_from_db
from app.db.sort_diary_messages import sort_diary_messages_timeorder
from app.utils.data_enum import AnalyzeUserField, DiaryField
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
    diary_list = get_all_diary_from_db(user_id)
    diaries_str = ""
    for diary in diary_list:
        year, month, day = diary[DiaryField.date.value].split("-")
        sorted_diary_messages = sort_diary_messages_timeorder(diary)
        diaries_str += (
            format_sorted_diary_to_llm_input(sorted_diary_messages, year, month, day)
            + "\n\n"
        )
        if (DiaryField.summary.value in diary) and (DiaryField.feedback.value in diary):
            diaries_str += format_llm_response_json_to_str(
                diary[DiaryField.summary.value], diary[DiaryField.feedback.value]
            )

    result = openai_call(
        system_prompt,
        summarize_diary_prompt.format(diaries=diaries_str),
        print_response=print_response,
        json_format=True,
    )

    result_dict = json.loads(result)

    personality = result_dict.get(AnalyzeUserField.personality.value, "")
    strength = result_dict.get(AnalyzeUserField.strength.value, "")
    weekness = result_dict.get(AnalyzeUserField.weakness.value, "")
    return personality, strength, weekness
