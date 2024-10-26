import os
from datetime import datetime
from typing import Any

from app.alg.db_storage import upload_to_gcs
from app.gcp_settings import db
from app.utils.data_enum import (
    DiaryCollection,
    DiaryField,
    FileField,
    RootCollection,
    TextField,
)
from app.utils.media_enum import MediaType
from app.utils.timestamp_format import (
    firestore_timestamp_to_datetime,
    timestamp_md_to_datetime,
)


def add_user_dairy_collection(
    user_id: str,
    timestamp: datetime,
):
    """ユーザーの日記コレクション(diary)を作成し、初日の日記ドキュメントを作成"""
    today = timestamp.strftime("%Y-%m-%d")
    diary_collection = (
        db.collection(RootCollection.diary.value)
        .document(user_id)
        .collection(DiaryCollection.diary.value)
    )
    diary_collection.document(today).set({DiaryField.date.value: today})
    print(f"Collection created: user: {user_id}")