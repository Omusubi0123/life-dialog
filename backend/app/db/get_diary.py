import os
from datetime import datetime
from typing import Any

from app.gcp_settings import db
from app.utils.data_enum import DiaryCollection, RootCollection


def get_diary_from_db(
    user_id: str,
    year: int,
    month: int,
    day: int,
) -> dict[str, Any]:
    """DBからユーザーの指定した日記を取得

    Args:
        user_id (str): LINEユーザーID
        year (int): 日記の年
        month (int): 日記の月
        day (int): 日記の日

    Returns:
        dict[str, Any]: 日記のアイテム
    """
    collection_name = os.path.join(
        RootCollection.diary.value, user_id, DiaryCollection.diary.value
    )
    diaries = db.collection(collection_name).list_documents()
    for diary in diaries:
        print(diary.id)
        print(diary.get().to_dict())
    exit()
    try:
        doc_ref = db.collection(collection_name).document(day)
    except Exception as e:
        print(f"Error: {e}")
        return []
    doc = doc_ref.get()
    doc_dict = doc.to_dict()
    return doc_dict


if __name__ == "__main__":
    data = {
        "user_id": "U304753f9739f31a9191e7b4e1543e9e1",
        "year": 2024,
        "month": 10,
        "day": 26,
    }
    get_diary_from_db(**data)
