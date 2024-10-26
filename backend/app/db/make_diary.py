import os
from datetime import datetime
from typing import Any

from app.gcp_settings import db
from app.utils.data_enum import (
    DiaryCollection,
    DiaryField,
    RootCollection,
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
