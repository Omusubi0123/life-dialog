from app.schemas.diary_schema import FileItem, TextItem
from app.utils.datetime_format import get_HMS_from_datetime


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