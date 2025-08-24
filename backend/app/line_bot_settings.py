from linebot import LineBotApi

from app.env_settings import env

line_bot_api = LineBotApi(env.channel_access_token)
