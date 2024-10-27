from linebot.models import QuickReply, TextMessage, TextSendMessage

from app.alg.summarize_diary import summarize_diary_by_llm
from app.alg.analyze_user import analyze_user_by_llm
from app.db.add_user_analization import add_user_analization
from app.db.add_diary_summary import add_diary_summary
from app.line_bot.flex_message import create_flex_message
from app.line_bot.quick_reply_item import create_quick_reply_buttons, create_reply_text
from app.utils.data_enum import QuickReplyField


def create_summary_feedback(event, year, month, day):
    """LLMによる日記の要約とフィードバックを作成"""
    user_id = event.source.user_id

    if event.message.text == QuickReplyField.view_diary.value:
        summary, feedback = summarize_diary_by_llm(user_id, year, month, day)
        add_diary_summary(user_id, summary, feedback, year, month, day)
        return summary, feedback
    else:
        return None, None


def create_quick_reply(
    event,
    user_status: str,
    year: int,
    month: int,
    day: int,
    summary: str = "",
    feedback: str = "",
    answer: str = "",
):
    """返信時に送信するquick replyを作成"""
    reply_text = create_reply_text(event, user_status, answer, feedback)
    quick_reply_buttons = create_quick_reply_buttons(user_status)
    quick_reply_message = TextSendMessage(
        text=reply_text, quick_reply=QuickReply(items=quick_reply_buttons)
    )

    messages = [quick_reply_message]
    # 日記閲覧はstatusに保存されないので、user_statusではなくevent.message.textで判定
    if isinstance(event.message, TextMessage):
        sent_text = event.message.text
    else:
        sent_text = None
    if sent_text == QuickReplyField.view_diary.value:
        flex_message = create_flex_message(
            event, user_status, summary, year, month, day
        )
        messages.insert(0, flex_message)
        
        personality, strength, weakness = analyze_user_by_llm(event.source.user_id)
        add_user_analization(event.source.user_id, personality, strength, weakness)

    return messages
