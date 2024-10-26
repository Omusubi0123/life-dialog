from datetime import datetime
import random

from linebot.models import (
    DatetimePickerTemplateAction,
    FlexSendMessage,
    MessageAction,
    QuickReply,
    QuickReplyButton,
    TextSendMessage,
)

from app.db.get_diary import get_diary_from_db
from app.alg.summarize_diary import summarize_diary_by_llm
from app.db.manage_user_status import get_user_status, update_user_status
from app.db.add_diary_summary import add_diary_summary
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
    
def create_summary_feedback(event, year, month, day):
  user_id = event.source.user_id

  if event.message.text == QuickReplyField.view_diary.value:
    summary, feedback = summarize_diary_by_llm(user_id, year, month, day)
    add_diary_summary(user_id, summary, feedback, year, month, day)
    return summary, feedback
  else:
      return None, None


def create_quick_reply_buttons(status):
    quick_reply_items = []
    images = []
    if status == QuickReplyField.diary_mode.value:
        quick_reply_items.append(QuickReplyField.interactive_mode.value)
        images.append(
            f"https://firebasestorage.googleapis.com/v0/b/{settings.gcs_bucket_name}/o/material%2Fdialogue_green.png?alt=media&token=51013bcc-86c8-4bca-9da4-d627e1b6424f"
        )
        images.append(
            f"https://firebasestorage.googleapis.com/v0/b/{settings.gcs_bucket_name}/o/material%2Fbook_green.png?alt=media&token=0d17b006-6bf7-4070-8454-ed7c967ef4d9"
        )
    elif status == QuickReplyField.interactive_mode.value:
        quick_reply_items.append(QuickReplyField.diary_mode.value)
        images.append(
            f"https://firebasestorage.googleapis.com/v0/b/{settings.gcs_bucket_name}/o/material%2Fpen_blue.png?alt=media&token=0ef43729-b0c8-4c4b-9d9c-7c9371d5b1c6"
        )
        images.append(
            f"https://firebasestorage.googleapis.com/v0/b/{settings.gcs_bucket_name}/o/material%2Fbook_blue.png?alt=media&token=bc5dd23f-3db0-4e81-aff3-9c60aab75fb3"
        )
    quick_reply_items.append(QuickReplyField.view_diary.value)

    quick_reply_buttons = [
        QuickReplyButton(action=MessageAction(label=item, text=item), image_url=image)
        for item, image in zip(quick_reply_items, images)
    ]

    return quick_reply_buttons

def create_reply_text(event, feedback):
    if event.message.text == QuickReplyField.diary_mode.value:
        return "【人生を記録】\n日々の生活を記録しよう！\n画像も送信できるよ♪"
    elif event.message.text == QuickReplyField.interactive_mode.value:
        return "【人生と対話】\n何について話す？\n日記を探すこともできるよ♪"
    elif event.message.text == QuickReplyField.view_diary.value:
        return feedback
    else:
        return "送信ありがとう♪"
    
def get_diary_random_image(user_id, year, month, day):
    doc_dict = get_diary_from_db(
        user_id, year, month, day
    )
    if 'files' in doc_dict and isinstance(doc_dict['files'], dict) and len(doc_dict['files']) > 0:
        # 'mediatype'が'image'のものだけを抽出
        image_files = [file_data['url'] for file_data in doc_dict['files'].values() if file_data['mediatype'] == 'image']
        
        if image_files:
            return random.choice(image_files)
        else:
            return None
    else:
        return None


def create_flex_message(event, status, summary, year, month, day):
    thumbnail_image_url = get_diary_random_image(event.source.user_id, year, month, day)
    print(thumbnail_image_url)

    if event.message.text == QuickReplyField.view_diary.value:
        flex_message = FlexSendMessage(
            alt_text="複数のカードメッセージ",
            contents={
                "type": "carousel",
                "contents": [
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": thumbnail_image_url if thumbnail_image_url else "https://firebasestorage.googleapis.com/v0/b/jp-hacks-77212.appspot.com/o/material%2Fdefault_diary_thumbnail.jpg?alt=media&token=9aad0b1e-04e4-4727-97a6-2668de248d02",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "今日の日記",
                                    "weight": "bold",
                                    "size": "xl",
                                },
                                {
                                    "type": "text",
                                    "text": f"{summary[:47]}...",
                                    "size": "md",
                                    "wrap": True,
                                },
                            ],
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
                                        "uri": f"{settings.frontend_url}?user_id={event.source.user_id}",
                                    },
                                }
                            ],
                        },
                    },
                ],
            },
        )
    elif status == QuickReplyField.interactive_mode.value:
        # TODO: 日記検索の場合は、探した日記をリンク付きで送信するのでflex_messageを作る必要がある
        flex_message = None
    else:
        flex_message = None
    return flex_message


def create_quick_reply(event, reply_text: str):
    user_id = event.source.user_id
    today = datetime.now()
    
    status = get_current_status(event)
    update_user_status(user_id, status)

    summary, feedback = create_summary_feedback(event, today.year, today.month, today.day)

    reply_text = create_reply_text(event, feedback)
    quick_reply_buttons = create_quick_reply_buttons(status)

    quick_reply_message = TextSendMessage(
        text=reply_text, quick_reply=QuickReply(items=quick_reply_buttons)
    )

    messages = [quick_reply_message]
    flex_message = create_flex_message(event, status, summary, today.year, today.month, today.day)
    if flex_message:
        messages.insert(0, flex_message)
    
    line_bot_api.reply_message(
        event.reply_token,
        messages
    )

