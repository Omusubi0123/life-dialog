from typing import Any

from app.gcp_settings import db
from app.utils.data_enum import RootCollection


def get_user_from_db(user_id: str) -> dict[str, Any]:
    """DBからユーザーのプロフィールを取得

    Args:
        user_id (str): LINEユーザーID

    Returns:
        dict[str, Any]: ユーザーのプロフィール
    """
    user_ref = db.collection(RootCollection.user.value).document(user_id)

    user = user_ref.get()
    user_dict = user.to_dict()
    return user_dict
