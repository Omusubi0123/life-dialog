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
    if status == QuickReplyField.diary_mode.value:
        quick_reply_items.append(QuickReplyField.interactive_mode.value)
    elif status == QuickReplyField.interactive_mode.value:
        quick_reply_items.append(QuickReplyField.diary_mode.value)
    quick_reply_items.append(QuickReplyField.view_diary.value)
    
    quick_reply_buttons = [
        QuickReplyButton(
            action=MessageAction(label=item, text=item),
            image_url="https://firebasestorage.googleapis.com/v0/b/jp-hacks-77212.appspot.com/o/image%2Fdiary.png?alt=media&token=267f1791-dbd1-4095-9c1a-e39eb7ade290"
        )
        for item in quick_reply_items
    ]

    return quick_reply_buttons

def create_flex_message(user_id: str):
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
                                    "uri": f"{settings.frontend_url}?user_id={user_id}"
                                }
                            }
                        ]
                    }
                },
            ]
        }
    )
    return flex_message

def create_quick_reply(event, reply_text: str):
    user_id = event.source.user_id
    status = get_current_status(event)
    update_user_status(user_id, status)
    quick_reply_buttons = create_quick_reply_buttons(status)

    flex_message = None
    if event.message.text == QuickReplyField.view_diary.value:
        flex_message = create_flex_message(user_id)
        reply_text = "この日は寝坊をしちゃったんだね。でも午後は数学の勉強を頑張れたみたいで良いじゃん！"

    quick_reply_message = TextSendMessage(
        text=reply_text,
        quick_reply=QuickReply(items=quick_reply_buttons)
    )

    messages = [quick_reply_message]
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

