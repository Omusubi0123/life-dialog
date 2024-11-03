from linebot.models import MessageAction, QuickReplyButton, TextMessage

from app.settings import settings
from app.utils.data_enum import QuickReplyField


def create_reply_text(event, user_status: str, answer: str, feedback: str) -> str:
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
        images.append(
            f"{settings.nginx_file_url}/material/dialogue_blue.png"
            # f"https://firebasestorage.googleapis.com/v0/b/{settings.gcs_bucket_name}/o/material%2Fdialogue_green.png?alt=media&token=51013bcc-86c8-4bca-9da4-d627e1b6424f"
        )
        images.append(
            f"{settings.nginx_file_url}/material/book_blue.png"
            # f"https://firebasestorage.googleapis.com/v0/b/{settings.gcs_bucket_name}/o/material%2Fbook_green.png?alt=media&token=0d17b006-6bf7-4070-8454-ed7c967ef4d9"
        )
    elif status == QuickReplyField.interactive_mode.value:
        quick_reply_items.append(QuickReplyField.diary_mode.value)
        images.append(
            f"{settings.nginx_file_url}/material/pen_green.png"
            # f"https://firebasestorage.googleapis.com/v0/b/{settings.gcs_bucket_name}/o/material%2Fpen_blue.png?alt=media&token=0ef43729-b0c8-4c4b-9d9c-7c9371d5b1c6"
        )
        images.append(
            f"{settings.nginx_file_url}/material/book_green.png"
            # f"https://firebasestorage.googleapis.com/v0/b/{settings.gcs_bucket_name}/o/material%2Fbook_blue.png?alt=media&token=bc5dd23f-3db0-4e81-aff3-9c60aab75fb3"
        )
    quick_reply_items.append(QuickReplyField.view_diary.value)

    quick_reply_buttons = [
        QuickReplyButton(action=MessageAction(label=item, text=item), image_url=image)
        for item, image in zip(quick_reply_items, images)
    ]

    return quick_reply_buttons
