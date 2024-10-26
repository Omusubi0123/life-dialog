from app.gcp_settings import db
from app.utils.data_enum import RootCollection


def update_user_status(user_id: str, status: str):
    """DBのユーザーステータス(記録モード or 対話モード)を更新"""
    db.collection(RootCollection.user.value).document(user_id).update(
        {"status": status}
    )


def get_user_status(user_id: str):
    """DBのユーザーステータス(記録モード or 対話モード)を取得"""
    return (
        db.collection(RootCollection.user.value)
        .document(user_id)
        .get()
        .to_dict()
        .get("status")
    )
