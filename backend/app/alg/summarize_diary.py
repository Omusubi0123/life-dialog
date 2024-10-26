import json

from app.alg.prompt.summarize_diary_prompt import SUMMARIZE_DIARY_PROMPT
from app.alg.prompt.system_prompt import SYSTEM_PROMPT_JSON
from app.db.get_diary import sort_diary_field_timeorder
from app.schemas.diary_schema import FileItem, TextItem
from app.utils.datetime_format import get_HMS_from_datetime
from app.utils.llm_response import openai_call


def format_sorted_diary_to_llm_input(
    sorted_diary_items: list[TextItem, FileItem],
    year: int,
    month: int,
    day: int,
) -> str:
    """DBから取得した日記のアイテムをLLMに入力する可読性の高い形式に変換する

    Args:
        sorted_diary_items (list[TextItem, FileItem]): 日記のアイテム

    Returns:
        str: LLMに入力する形式の文字列
    """
    date = f"Day: {year}年{month}月{day}日\n"
    diary_entries = []
    for item in sorted_diary_items:
        hour, minute, second = get_HMS_from_datetime(item.timestamp)
        entry_lines = [f"- {hour}:{minute}:{second}"]
        entry_lines.extend(
            [
                f"  {key}: {value}"
                for key, value in item.model_dump(exclude={"timestamp"}).items()
            ]
        )
        diary_entries.append("\n".join(entry_lines))
    return date + "\n".join(diary_entries)


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
    sorted_diary_items = sort_diary_field_timeorder(user_id, year, month, day)
    diary_str = format_sorted_diary_to_llm_input(sorted_diary_items, year, month, day)

    result = openai_call(
        system_prompt,
        summarize_diary_prompt.format(diary=diary_str),
        print_response=print_response,
        json_format=True,
    )

    result_dict = json.loads(result)

    summary = result_dict.get("summary", "")
    feedback = result_dict.get("feedback", "")
    return summary, feedback
