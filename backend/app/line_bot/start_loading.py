import requests

from app.settings import settings


def start_loading(chat_id, loading_seconds=5):
    """メッセージ応答までのローディングアニメーションを開始する"""
    url = "https://api.line.me/v2/bot/chat/loading/start"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.channel_access_token}",
    }
    data = {"chatId": chat_id, "loadingSeconds": loading_seconds}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Loading animation started:", response.json())
    else:
        print("Error starting loading animation:", response.status_code, response.text)
