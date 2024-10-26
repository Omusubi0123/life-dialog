import os
from datetime import datetime
from typing import Any

from app.alg.format_diary_for_llm import format_sorted_diary_to_llm_input
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
    day = datetime(year, month, day).strftime("%Y-%m-%d")
    collection_name = os.path.join(
        RootCollection.diary.value, user_id, DiaryCollection.diary.value
    )
    try:
        doc_ref = db.collection(collection_name).document(day)
    except Exception as e:
        print(f"Error: {e}")
        return []
    doc = doc_ref.get()
    doc_dict = doc.to_dict()
    return doc_dict


def get_all_diary_from_db(user_id: str) -> list[dict[str, Any]]:
    """DBからユーザーの全日記を取得"""
    collection_name = os.path.join(
        RootCollection.diary.value, user_id, DiaryCollection.diary.value
    )
    diaries = db.collection(collection_name).list_documents()
    diary_list = [diary.get().to_dict() for diary in diaries]

    return diary_list
