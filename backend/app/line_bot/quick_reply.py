from datetime import datetime

from linebot.models import QuickReply, TextSendMessage

from app.alg.summarize_diary import summarize_diary_by_llm
from app.db.add_diary_summary import add_diary_summary
from app.db.manage_user_status import get_user_status, update_user_status
from app.line_bot.flex_message import create_flex_message
from app.line_bot.quick_reply_item import create_quick_reply_buttons, create_reply_text
from app.line_bot_settings import line_bot_api
from app.utils.data_enum import QuickReplyField


def get_current_status(event):
    """現在のステータス(記録モード or 対話モード)を取得"""
    if event.message.text == QuickReplyField.diary_mode.value:
        return QuickReplyField.diary_mode.value
    elif event.message.text == QuickReplyField.interactive_mode.value:
        return QuickReplyField.interactive_mode.value
    else:
        return get_user_status(event.source.user_id)


def create_summary_feedback(event, year, month, day):
    """LLMによる日記の要約とフィードバックを作成"""
    user_id = event.source.user_id

    if event.message.text == QuickReplyField.view_diary.value:
        summary, feedback = summarize_diary_by_llm(user_id, year, month, day)
        add_diary_summary(user_id, summary, feedback, year, month, day)
        return summary, feedback
    else:
        return None, None


def create_quick_reply(event):
    """返信時に送信するquick replyを作成"""
    user_id = event.source.user_id
    today = datetime.now()
    status = get_current_status(event)
    text = event.message.text

    if text in QuickReplyField.get_values() and text != status:
        update_user_status(user_id, status)

    summary, feedback = create_summary_feedback(
        event, today.year, today.month, today.day
    )

    reply_text = create_reply_text(event, feedback)
    quick_reply_buttons = create_quick_reply_buttons(status)

    quick_reply_message = TextSendMessage(
        text=reply_text, quick_reply=QuickReply(items=quick_reply_buttons)
    )

    messages = [quick_reply_message]
    flex_message = create_flex_message(
        event, status, summary, today.year, today.month, today.day
    )
    if flex_message:
        messages.insert(0, flex_message)

    line_bot_api.reply_message(event.reply_token, messages)
