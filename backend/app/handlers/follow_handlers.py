import requests

from app.settings import Settings
from app.utils.timestamp_format import timestamp_md_to_datetime
from backend.app.db.add_user import add_user_document
from backend.app.db.make_diary import add_user_dairy_collection

settings = Settings()
channel_access_token = settings.channel_access_token


def handle_follow_event(event):
    """公式アカウントに登録された時、ユーザードキュメントと日記コレクションを作成"""
    user_id = event.source.user_id
    timestamp = timestamp_md_to_datetime(event.timestamp)

    url = f"https://api.line.me/v2/bot/user/{user_id}/linkToken"
    headers = {
        "Authorization": f"Bearer {channel_access_token}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print("Success:", response.json())
        link_token = response.json()["linkToken"]
        user_doc_field = {
            "user_id": user_id,
            "timestamp": timestamp,
            "linkToken": link_token,
        }
        add_user_document(user_id, user_doc_field)
        add_user_dairy_collection(user_id, timestamp)
        print(f"Follow Event: user_id: {user_id}, timestamp: {timestamp}")
