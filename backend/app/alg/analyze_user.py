import json

from app.alg.format_diary_for_llm import format_sorted_diary_to_llm_input
from app.alg.prompt.summarize_diary_prompt import SUMMARIZE_DIARY_PROMPT
from app.alg.prompt.system_prompt import SYSTEM_PROMPT_JSON
from app.db.get_diary import get_all_diary_from_db
from app.db.sort_diary_messages import sort_diary_messages_timeorder
from app.utils.data_enum import DiaryField
from app.utils.llm_response import openai_call


def analyze_user_by_llm(
    user_id: str,
    system_prompt: str = SYSTEM_PROMPT_JSON,
    summarize_diary_prompt: str = SUMMARIZE_DIARY_PROMPT,
    print_response: bool = True,
) -> tuple[str, str]:
    """ユーザーの全日記からユーザーの性格・強み・弱みをLLMで生成する

    Returns:
        LLMによる日記の要約
    """
    diary_list = get_all_diary_from_db(user_id)
    diaries_str = ""
    for diary in diary_list:
        year, month, day = diary[DiaryField.date.value].split("-")
        diaries_str += (
            format_sorted_diary_to_llm_input(diary, year, month, day) + "\n\n"
        )

    result = openai_call(
        system_prompt,
        summarize_diary_prompt.format(diaries=diaries_str),
        print_response=print_response,
        json_format=True,
    )

    result_dict = json.loads(result)

    summary = result_dict.get(DiaryField.summary.value, "")
    feedback = result_dict.get(DiaryField.feedback.value, "")
    return summary, feedback
