import requests

from app.db.db_insert import add_user
from app.settings import settings
from app.utils.data_enum import QuickReplyField
from app.utils.session_scope import get_session

channel_access_token = settings.channel_access_token


def get_user_profile(user_id: str) -> dict | None:
    """ユーザーのプロフィール情報を取得

    Args:
        user_id (str): LINEユーザーID

    Returns:
        dict | None: ユーザーのプロフィール情報
    """
    url = f"https://api.line.me/v2/bot/profile/{user_id}"
    headers = {"Authorization": f"Bearer {settings.channel_access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Success:", response.json())
        return response.json()
    else:
        return None


def get_user_link_token(user_id: str) -> str | None:
    """LINEユーザーIDからlinkTokenを取得

    Args:
        user_id (str): LINEユーザーID

    Returns:
        str | None: linkToken
    """
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
    """公式アカウントに登録された時、ユーザーテーブルにユーザー情報を追加

    Args:
        event (_type_): LINEイベント
    """
    user_id = event.source.user_id

    link_token = get_user_link_token(user_id)
    user_profile = get_user_profile(user_id)

    if link_token and user_profile:
        with get_session() as session:
            add_user(
                session,
                user_id=user_id,
                name=user_profile["displayName"],
                mode=QuickReplyField.diary_mode.value,
                icon_url=user_profile["pictureUrl"]
                if "pictureUrl" in user_profile
                else "",
                status_message=user_profile["statusMessage"]
                if "statusMessage" in user_profile
                else "",
                link_token=link_token,
            )

        print(f"Follow Event: user_id: {user_id}")
