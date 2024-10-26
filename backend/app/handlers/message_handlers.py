from linebot import LineBotApi
from linebot.models import TextSendMessage

from app.db.write_diary import update_doc_field
from app.line_bot.quick_reply import create_quick_reply
from app.settings import Settings
from app.utils.media_enum import MediaType

settings = Settings()
line_bot_api = LineBotApi(settings.channel_access_token)


def handle_text_message(event):
    """テキストメッセージをDBに保存しオウム返し"""
    user_id = event.source.user_id
    message_id = event.message.id
    text = event.message.text
    timestamp = event.timestamp
    reply_text = update_doc_field(
        user_id, message_id, text, MediaType.TEXT.value, timestamp
    )
    create_quick_reply(event, reply_text)


def handle_media_message(event):
    """画像ファイルをDBに保存しURLを返す"""
    user_id = event.source.user_id
    message_id = event.message.id
    media_type = event.message.type
    timestamp = event.timestamp
    message_content = line_bot_api.get_message_content(message_id)
    reply_url = update_doc_field(
        user_id, message_id, message_content, media_type, timestamp
    )
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_url))
