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


def create_flex_message(user_id: str):
    flex_message = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "Welcome to our service!",
                    "weight": "bold",
                    "size": "xl",
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Check out our services below:",
                            "size": "sm",
                            "color": "#999999",
                        }
                    ],
                },
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "uri",
                        "label": "Visit Website",
                        "uri": f"{settings.frontend_url}?user_id={user_id}",
                    },
                },
            ],
        },
    }
    return flex_message

def create_quick_reply(event, reply_text: str):
    user_id = event.source.user_id
    flex_message = None
    
    quick_reply_items = []
    if event.message.text == QuickReplyField.view_diary.value:
        flex_message = FlexSendMessage(
            alt_text="Welcome Message",
            contents=create_flex_message(user_id)
        )
    elif event.message.text == QuickReplyField.diary_mode.value:
        update_user_status(user_id, QuickReplyField.diary_mode.value)
    elif event.message.text == QuickReplyField.interactive_mode.value:
        update_user_status(user_id, QuickReplyField.interactive_mode.value)

    quick_reply_items.append(QuickReplyField.diary_mode.value)
    quick_reply_items.append(QuickReplyField.interactive_mode.value)
    quick_reply_items.append(QuickReplyField.view_diary.value)
    
    quick_reply_buttons = [
        QuickReplyButton(
            action=MessageAction(label=item, text=item),
            image_url="https://firebasestorage.googleapis.com/v0/b/jp-hacks-77212.appspot.com/o/image%2Fdiary.png?alt=media&token=267f1791-dbd1-4095-9c1a-e39eb7ade290"
        )
        for item in quick_reply_items
    ]

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


#     # 全てのモードで「日付選択」は表示する
#     # extra_items = [QuickReplyField.day_choice.value]
#     # datetime_picker_action = DatetimePickerTemplateAction(
#     #     label=QuickReplyField.day_choice.value,
#     #     data="action=select_date",
#     #     mode="date",
#     #     initial="2024-04-24",
#     #     min="2024-01-01",
#     #     max="2024-12-31",
#     # )
#     # quick_reply_buttons += [
#     #     QuickReplyButton(action=datetime_picker_action, image_url=image_url)
#     #     for item in extra_items
#     # ]
#     quick_reply = QuickReply(items=quick_reply_buttons)
#     line_bot_api.reply_message(
#         event.reply_token, TextSendMessage(text=reply_text, quick_reply=quick_reply)
#     )