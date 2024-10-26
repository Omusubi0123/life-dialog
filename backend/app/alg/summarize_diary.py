import json

from app.alg.format_diary_for_llm import format_sorted_diary_to_llm_input
from app.alg.prompt.summarize_diary_prompt import SUMMARIZE_DIARY_PROMPT
from app.alg.prompt.system_prompt import SYSTEM_PROMPT_JSON
from app.db.get_diary import get_diary_from_db, sort_diary_messages_timeorder
from app.utils.data_enum import DiaryField
from app.utils.llm_response import openai_call


def summarize_diary_by_llm(
    user_id: str,
    year: int,
    month: int,
    day: int,
    system_prompt: str = SYSTEM_PROMPT_JSON,
    summarize_diary_prompt: str = SUMMARIZE_DIARY_PROMPT,
    print_response: bool = True,
) -> tuple[str, str]:
    """日記から1日の出来事の要約をLLMで生成する

    Returns:
        LLMによる日記の要約
    """
    doc_dict = get_diary_from_db(user_id, year, month, day)
    sorted_diary_items = sort_diary_messages_timeorder(doc_dict)
    diary_str = format_sorted_diary_to_llm_input(sorted_diary_items, year, month, day)

    result = openai_call(
        system_prompt,
        summarize_diary_prompt.format(diary=diary_str),
        print_response=print_response,
        json_format=True,
    )

    result_dict = json.loads(result)

    summary = result_dict.get(DiaryField.summary.value, "")
    feedback = result_dict.get(DiaryField.feedback.value, "")
    return summary, feedback
