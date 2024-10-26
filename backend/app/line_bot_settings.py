from linebot import LineBotApi

from app.settings import settings

line_bot_api = LineBotApi(settings.channel_access_token)
