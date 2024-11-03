from datetime import date

from app.db.model import Message


def format_messages_to_llm_input(
    messages: list[Message],
    date: date,
) -> str:
    """DBから取得したメッセージをLLMに入力する可読性の高い形式に変換する

    Args:
        messages (list[Message]): メッセージ

    Returns:
        str: LLMに入力する形式の文字列
    """
    date = f"Day: {date.year}年{date.month}月{date.day}日\n"
    message_entries = []
    for message in messages:
        entry_lines = [f"- {message['sent_at']}"]
        entry_lines.append(f"  media_type: {message['media_type']}")
        entry_lines.append(f"  content: {message['content']}")
        message_entries.append("\n".join(entry_lines))
    return date + "\n".join(message_entries)


def format_llm_response_json_to_str(
    title: str,
    summary: str,
    feedback: str,
) -> str:
    """LLMの出力を可読性の高い形式に変換する

    Args:
        title (str): 日記のタイトル
        summary (str): 日記の要約
        feedback (str): フィードバック

    Returns:
        str: 可読性の高い形式の文字列
    """
    return f"Title: {title}\nSummary: {summary}\nFeedback: {feedback}\n"
