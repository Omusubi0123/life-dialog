from linebot.models import MessageAction, QuickReplyButton, TextMessage

from app.env_settings import env
from app.utils.data_enum import QuickReplyField


def create_reply_text(
    event, user_status: str, answer: str, feedback: str, auth_message: str
) -> str:
    """quick replyのボタンに対応したテキストを返す

    Args:
        event (_type_): LINEイベント
        user_status (str): 現在のユーザーステータス
        answer (str): LLMによる日記の要約
        feedback (str): LLMによる日記のフィードバック

    Returns:
        str: quick replyのボタンに対応したテキスト
    """
    if isinstance(event.message, TextMessage):
        sent_text = event.message.text
    else:
        sent_text = None

    if sent_text == QuickReplyField.diary_mode.value:
        return "【人生を記録】\n日々の生活を記録しよう！\n画像も送信できるよ♪"
    elif sent_text == QuickReplyField.interactive_mode.value:
        return "【人生と対話】\n何について話す？\n日記を探すこともできるよ♪\n対話のやり取りは保存されないから注意してね(^^♪"
    elif sent_text == QuickReplyField.view_diary.value:
        return feedback
    elif sent_text == QuickReplyField.web_auth.value:
        return auth_message
    elif user_status == QuickReplyField.interactive_mode.value:
        if sent_text:
            return answer
        else:
            return "素敵な写真だね♪"
    else:
        return "送信ありがとう♪"


def create_quick_reply_buttons(status: str) -> list:
    """quick replyのボタンを作成

    Args:
        status (str): 現在のユーザーステータス

    Returns:
        list: quick replyのボタン
    """
    quick_reply_items = []
    images = []
    if status == QuickReplyField.diary_mode.value:
        quick_reply_items.append(QuickReplyField.interactive_mode.value)
        images.append(f"{env.nginx_file_url}/material/dialogue_blue.png")
    elif status == QuickReplyField.interactive_mode.value:
        quick_reply_items.append(QuickReplyField.diary_mode.value)
        images.append(f"{env.nginx_file_url}/material/pen_blue.png")
    quick_reply_items.append(QuickReplyField.view_diary.value)
    images.append(f"{env.nginx_file_url}/material/book_blue.png")

    quick_reply_items.append(QuickReplyField.web_auth.value)
    images.append(f"{env.nginx_file_url}/material/book_green.png")

    quick_reply_buttons = [
        QuickReplyButton(action=MessageAction(label=item, text=item), image_url=image)
        for item, image in zip(quick_reply_items, images)
    ]

    return quick_reply_buttons
