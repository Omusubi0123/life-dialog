from app.gcp_settings import db
from app.utils.data_enum import RootCollection


def add_user_document(
    user_id: str,
    field: dict,
):
    """友達追加したユーザーのユーザードキュメントを作成"""
    db.collection(RootCollection.user.value).document(user_id).set(field)
    print(f"Document created: user: {user_id}, {field}")


def update_user_status(user_id: str, status: str):
    db.collection(RootCollection.user.value).document(user_id).update(
        {"status": status}
    )


def get_user_status(user_id: str):
    return (
        db.collection(RootCollection.user.value)
        .document(user_id)
        .get()
        .to_dict()
        .get("status")
    )
