from linebot.models import (
    DatetimePickerTemplateAction,
    FlexSendMessage,
    MessageAction,
    QuickReply,
    QuickReplyButton,
    TextSendMessage,
)

from app.db.manage_user_status import get_user_status, update_user_status
from app.line_bot_settings import line_bot_api
from app.settings import settings
from app.utils.data_enum import QuickReplyField

def get_current_status(event):
    if event.message.text == QuickReplyField.diary_mode.value:
        return QuickReplyField.diary_mode.value
    elif event.message.text == QuickReplyField.interactive_mode.value:
        return QuickReplyField.interactive_mode.value
    else:
        return get_user_status(event.source.user_id)

def create_quick_reply_buttons(status):
    quick_reply_items = []
    images = []
    if status == QuickReplyField.diary_mode.value:
        quick_reply_items.append(QuickReplyField.interactive_mode.value)
        images.append(f"https://firebasestorage.googleapis.com/v0/b/{settings.gcs_bucket_name}/o/material%2Fdialogue_green.png?alt=media&token=51013bcc-86c8-4bca-9da4-d627e1b6424f")
        images.append(f"https://firebasestorage.googleapis.com/v0/b/{settings.gcs_bucket_name}/o/material%2Fbook_green.png?alt=media&token=0d17b006-6bf7-4070-8454-ed7c967ef4d9")
    elif status == QuickReplyField.interactive_mode.value:
        quick_reply_items.append(QuickReplyField.diary_mode.value)
        images.append(f"https://firebasestorage.googleapis.com/v0/b/{settings.gcs_bucket_name}/o/material%2Fpen_blue.png?alt=media&token=0ef43729-b0c8-4c4b-9d9c-7c9371d5b1c6")
        images.append(f"https://firebasestorage.googleapis.com/v0/b/{settings.gcs_bucket_name}/o/material%2Fbook_blue.png?alt=media&token=bc5dd23f-3db0-4e81-aff3-9c60aab75fb3")
    quick_reply_items.append(QuickReplyField.view_diary.value)

    quick_reply_buttons = [
        QuickReplyButton(
            action=MessageAction(label=item, text=item),
            image_url=f"https://firebasestorage.googleapis.com/v0/b/{settings.gcs_bucket_name}/o/material%2Fbook_blue.png?alt=media&token=bc5dd23f-3db0-4e81-aff3-9c60aab75fb3"
        )
        for item, image in zip(quick_reply_items, images)
    ]

    return quick_reply_buttons

def create_reply_text(event):
    if event.message.text == QuickReplyField.diary_mode.value:
        return "【人生を記録】\n日々の生活を記録しよう！\n画像も送信できるよ♪"
    elif event.message.text == QuickReplyField.interactive_mode.value:
        return "【人生と対話】\n何について話す？\n日記を探すこともできるよ♪"
    elif event.message.text == QuickReplyField.view_diary.value:
        # return "この日は寝坊をしちゃったんだね。でも午後は数学の勉強を頑張れたみたいで良いじゃん！"
        return "日記に対するLLMのフィードバック"
    else:
        return "送信ありがとう♪"

def create_flex_message(event, status):
    if status == QuickReplyField.interactive_mode.value:
        # TODO: 日記検索の場合は、探した日記をリンク付きで送信するのでflex_messageを作る必要がある
        flex_message = None
    elif event.message.text == QuickReplyField.view_diary.value:
        # TODO: image urlを日記の画像にする
        flex_message = FlexSendMessage(
            alt_text='複数のカードメッセージ',
            contents={
                "type": "carousel",
                "contents": [
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://page.mkgr.jp/ownedmedia/wordpress/wp-content/uploads/2023/11/image1-1.jpg",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "今日の日記",
                                    "weight": "bold",
                                    "size": "xl"
                                },
                                {
                                    "type": "text",
                                    "text": "この日は図書館で勉強を頑張り、家に帰ってからはドラマを見た。夜ご飯は好物をお母さんが作ってくれて...",
                                    "size": "md",
                                    "wrap": True
                                }
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "uri",
                                        "label": "この日記を見る",
                                        "uri": f"{settings.frontend_url}?user_id={event.source.user_id}"
                                    }
                                }
                            ]
                        }
                    },
                ]
            }
        )
    else:
        flex_message = None
    return flex_message

def create_quick_reply(event, reply_text: str):
    user_id = event.source.user_id
    status = get_current_status(event)
    update_user_status(user_id, status)
    reply_text = create_reply_text(event)
    quick_reply_buttons = create_quick_reply_buttons(status)

    quick_reply_message = TextSendMessage(
        text=reply_text,
        quick_reply=QuickReply(items=quick_reply_buttons)
    )

    messages = [quick_reply_message]
    flex_message = create_flex_message(event, status)
    if flex_message:
        messages.insert(0, flex_message)
    
    line_bot_api.reply_message(
        event.reply_token,
        messages
    )

    quick_reply = QuickReply(items=quick_reply_buttons)
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=reply_text, quick_reply=quick_reply)
    )

