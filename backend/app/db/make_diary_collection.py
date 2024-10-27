import uuid
from datetime import datetime

from app.gcp_settings import db
from app.utils.data_enum import DiaryCollection, DiaryField, RootCollection


def add_user_dairy_collection(
    user_id: str,
    timestamp: datetime,
):
    """ユーザーの日記コレクション(diary)を作成し、初日の日記ドキュメントを作成

    Args:
        user_id (str): LINEユーザーID
        timestamp (datetime): 日記を書いた日時
    """
    today = timestamp.strftime("%Y-%m-%d")
    diary_collection = (
        db.collection(RootCollection.diary.value)
        .document(user_id)
        .collection(DiaryCollection.diary.value)
    )

    random_id = str(uuid.uuid4())
    doc_data = {
        DiaryField.date.value: today,
        DiaryField.diary_id.value: random_id,
    }
    diary_collection.document(today).set(doc_data)
    print(f"Collection created: user: {user_id}")
