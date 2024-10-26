import os
from datetime import datetime
from typing import Any

from app.alg.summarize_diary import summarize_diary_by_llm
from app.gcp_settings import db
from app.utils.data_enum import DiaryCollection, DiaryField, RootCollection


def add_diary_summary(
    user_id: str,
    year: int,
    month: int,
    day: int,
) -> tuple[str, str]:
    """指定した日付の日記の 要約 + フィードバック を生成しDBに保存

    Args:
        user_id (str): LINEユーザーID
        year (int): 日記の年
        month (int): 日記の月
        day (int): 日記の日

    Returns:
        Any: 日記のアイテム
    """
    summary, feedback = summarize_diary_by_llm(user_id, year, month, day)
    day = datetime(year, month, day).strftime("%Y-%m-%d")
    collection_name = os.path.join(
        RootCollection.diary.value, user_id, DiaryCollection.diary.value
    )

    doc_ref = db.collection(collection_name).document(day)
    doc_dict = doc_ref.get().to_dict()
    doc_dict[DiaryField.summary.value] = summary
    doc_dict[DiaryField.feedback.value] = feedback
    doc_ref.set(doc_dict)
    print(f"Summary and feedback added to diary: {day}\nUserID: {user_id}")

    return summary, feedback


if __name__ == "__main__":
    data = {
        "user_id": "U304753f9739f31a9191e7b4e1543e9e1",
        "year": 2024,
        "month": 10,
        "day": 26,
    }
    add_diary_summary(**data)
