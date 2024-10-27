from app.gcp_settings import db
from app.utils.data_enum import RootCollection


def add_user_document(
    user_id: str,
    field: dict,
):
    """友達追加したユーザーのユーザードキュメントを作成

    Args:
        user_id (str): LINEユーザーID
        field (dict): 日記ドキュメントのフィールド
    """
    db.collection(RootCollection.user.value).document(user_id).set(field)
    print(f"Document created: user: {user_id}, {field}")
