from linebot.models import (
    DatetimePickerTemplateAction,
    FlexSendMessage,
    MessageAction,
    QuickReply,
    QuickReplyButton,
    TextSendMessage,
)

from app.db.user import get_user_status, update_user_status
from app.line_bot_settings import line_bot_api
from app.utils.data_enum import QuickReplyField
from app.settings import settings


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
    # 「日記モード」、「対話モード」、とそれ以外を分ける
    # 「日記閲覧」以外の項目も追加する
    if event.message.text in [QuickReplyField.view_diary.value]:
        if event.message.text == QuickReplyField.view_diary.value:
            flex_message = create_flex_message(user_id)
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Welcome Message", contents=flex_message),
            )
    else:
        if event.message.text == QuickReplyField.diary_mode.value:
            update_user_status(user_id, QuickReplyField.diary_mode.value)
            items = [QuickReplyField.diary_mode.value]
            image_url = "https://firebasestorage.googleapis.com/v0/b/jp-hacks-77212.appspot.com/o/image%2Fdiary.png?alt=media&token=267f1791-dbd1-4095-9c1a-e39eb7ade290"
        elif event.message.text == QuickReplyField.interactive_mode.value:
            update_user_status(user_id, QuickReplyField.interactive_mode.value)
            items = [QuickReplyField.interactive_mode.value]
            image_url = "https://firebasestorage.googleapis.com/v0/b/jp-hacks-77212.appspot.com/o/image%2Fcommunication.png?alt=media&token=2c99c831-0243-48b5-bbb4-5d5258309233"
        else:
            user_status = get_user_status(user_id)
            items = [user_status]
            if user_status == QuickReplyField.diary_mode.value:
                image_url = "https://firebasestorage.googleapis.com/v0/b/jp-hacks-77212.appspot.com/o/image%2Fcommunication.png?alt=media&token=2c99c831-0243-48b5-bbb4-5d5258309233"
            else:
                image_url = "https://firebasestorage.googleapis.com/v0/b/jp-hacks-77212.appspot.com/o/image%2Fdiary.png?alt=media&token=267f1791-dbd1-4095-9c1a-e39eb7ade290"
        items += [QuickReplyField.view_diary.value]
        quick_reply_buttons = [
            QuickReplyButton(
                action=MessageAction(label=item, text=item), image_url=image_url
            )
            for item in items
        ]

        # 全てのモードで「日付選択」は表示する
        extra_items = [QuickReplyField.day_choice.value]
        datetime_picker_action = DatetimePickerTemplateAction(
            label=QuickReplyField.day_choice.value,
            data="action=select_date",
            mode="date",
            initial="2024-04-24",
            min="2024-01-01",
            max="2024-12-31",
        )
        quick_reply_buttons += [
            QuickReplyButton(action=datetime_picker_action, image_url=image_url)
            for item in extra_items
        ]
        quick_reply = QuickReply(items=quick_reply_buttons)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=reply_text, quick_reply=quick_reply)
        )
