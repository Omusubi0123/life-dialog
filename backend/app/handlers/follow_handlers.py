import requests

from app.db.add_user import add_user_document
from app.db.make_diary_collection import add_user_dairy_collection
from app.settings import Settings
from app.utils.data_enum import UserField
from app.utils.timestamp_format import timestamp_md_to_datetime

settings = Settings()
channel_access_token = settings.channel_access_token


def get_user_profile(user_id):
    url = f'https://api.line.me/v2/bot/profile/{user_id}'
    headers = {
        'Authorization': f'Bearer {settings.channel_access_token}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Success:", response.json())
        return response.json()
    else:
        return None

def get_user_link_token(user_id):
    url = f"https://api.line.me/v2/bot/user/{user_id}/linkToken"
    headers = {
        "Authorization": f"Bearer {channel_access_token}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print("Success:", response.json())
        link_token = response.json()["linkToken"]
        return link_token
    else:
        return None

def handle_follow_event(event):
    """公式アカウントに登録された時、ユーザードキュメントと日記コレクションを作成"""
    user_id = event.source.user_id
    timestamp = timestamp_md_to_datetime(event.timestamp)
    
    link_token = get_user_link_token(user_id)
    user_profile = get_user_profile(user_id)

    if link_token and user_profile:
        user_doc_field = {
            UserField.user_id.value: user_id,
            UserField.user_name.value: user_profile["displayName"],
            UserField.icon_url.value: user_profile["pictureUrl"] if "pictureUrl" in user_profile else "",
            UserField.status_message.value: user_profile["statusMessage"] if "statusMessage" in user_profile else "",
            UserField.created_at.value: timestamp,
            UserField.linkToken.value: link_token,
        }
        add_user_document(user_id, user_doc_field)
        add_user_dairy_collection(user_id, timestamp)
        print(f"Follow Event: user_id: {user_id}, timestamp: {timestamp}")
