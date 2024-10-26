from app.utils.llm_response import openai_call
from app.db.get_diary import sort_diary_field_timeorder
from app.schemas.diary_schema import FileItem, TextItem
from app.alg.prompt.system_prompt import SYSTEM_PROMPT
from app.alg.prompt.summarize_diary_prompt import SUMMARIZE_DIARY_PROMPT


def format_sorted_diary_to_llm_input(sorted_diary_items: list[TextItem, FileItem]) -> str:
    """DBから取得した日記のアイテムをLLMに入力する可読性の高い形式に変換する

    Args:
        sorted_diary_items (list[TextItem, FileItem]): 日記のアイテム

    Returns:
        str: LLMに入力する形式の文字列
    """    
    diary_entries = []
    for item in sorted_diary_items:
        entry_lines = [f"- {item.timestamp}:"]
        entry_lines.extend(
            [f"  {key}: {value}" for key, value in item.model_dump(exclude={'timestamp'}).items()]
        )   
        diary_entries.append("\n".join(entry_lines))
    return "\n".join(diary_entries)


def summarize_diary_by_llm(
    user_id: str,
    year: int,
    month: int,
    day: int,
    system_prompt: str = SYSTEM_PROMPT,
    summarize_diary_prompt: str = SUMMARIZE_DIARY_PROMPT,
    print_response: bool = True,
):
    """日記から1日の出来事の要約をLLMで生成する

    Returns:
        LLMによる日記の要約
    """    
    sorted_diary_items = sort_diary_field_timeorder(user_id, year, month, day)
    diary_str = format_sorted_diary_to_llm_input(sorted_diary_items)
    print(diary_str)
    summary = openai_call(
        system_prompt,
        summarize_diary_prompt.format(diary=diary_str),
        print_response=print_response,
    )
    return summary

