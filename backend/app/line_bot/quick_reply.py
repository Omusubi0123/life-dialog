from datetime import date

from linebot.models import QuickReply, TextMessage, TextSendMessage

from app.line_bot.flex_message import create_flex_message
from app.line_bot.quick_reply_item import create_quick_reply_buttons, create_reply_text
from app.utils.data_enum import QuickReplyField


def create_quick_reply(
    event,
    user_status: str,
    date: date,
    summary: str = "",
    feedback: str = "",
    answer: str = "",
    date_list: list = [],
    user_id_list: list = [],
) -> list:
    """返信時に送信するquick replyを作成

    Args:
        event (_type_): LINEイベント
        user_status (str): 現在のユーザーステータス
        year (int): 今日の年
        month (int): 今日の月
        day (int): 今日の日
        summary (str, optional): LLMによる日記の要約. Defaults to "".
        feedback (str, optional): LLMによる日記のフィードバック. Defaults to "".
        answer (str, optional): LLMによる対話の質問への回答. Defaults to "".
        date_list (list, optional): RAGにより取得した日揮のdateのリスト. Defaults to [].
        user_id_list (list, optional) RAGにより取得した日記のユーザーID. Defaults to [].

    Returns:
        list: 送信するメッセージ
    """
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
    if sent_text == QuickReplyField.view_diary.value or (
        user_status == QuickReplyField.interactive_mode.value
        and date_list
        and user_id_list
    ):
        flex_message = create_flex_message(
            event, user_status, summary, date, date_list, user_id_list
        )
        if sent_text == QuickReplyField.view_diary.value or (
            user_status == QuickReplyField.interactive_mode.value
            and date_list
            and user_id_list
        ):
            messages.insert(0, flex_message)
    return messages
