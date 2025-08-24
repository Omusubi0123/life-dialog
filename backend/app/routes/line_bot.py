from fastapi import APIRouter, Request
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    AudioMessage,
    FollowEvent,
    ImageMessage,
    MessageEvent,
    TextMessage,
    VideoMessage,
)

from app.env_settings import env
from app.handlers.follow_handlers import handle_follow_event
from app.handlers.message_handlers import handle_media_message, handle_text_message

line_bot_router = APIRouter()

handler = WebhookHandler(env.channel_secret)


@line_bot_router.post("/callback")
async def callback(request: Request):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        return {"message": "Invalid signature"}

    return {"message": "OK"}


handler.add(MessageEvent, message=TextMessage)(handle_text_message)
handler.add(MessageEvent, message=ImageMessage)(handle_media_message)
handler.add(MessageEvent, message=VideoMessage)(handle_media_message)
handler.add(MessageEvent, message=AudioMessage)(handle_media_message)
handler.add(FollowEvent)(handle_follow_event)
