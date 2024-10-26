import json
import os
from datetime import datetime
from typing import Any

from app.gcp_settings import db
from app.schemas.diary_schema import FileItem, TextItem
from app.utils.data_enum import (
    DiaryCollection,
    DiaryField,
    FileField,
    RootCollection,
    TextField,
)
from app.utils.timestamp_format import firestore_timestamp_to_datetime


def convert_timestamps(
    fields: dict[str, Any], timestamp_field: str
) -> list[dict[str, Any]]:
    """タイムスタンプをdatetimeオブジェクトに変換するヘルパー関数"""
    result_list = []
    for item in fields.values():
        item[timestamp_field] = firestore_timestamp_to_datetime(item[timestamp_field])
        result_list.append(item)
    return result_list


def sort_diary_field_timeorder(
    user_id: str,
    year: int,
    month: int,
    day: int,
    print_diary: bool = False,
) -> list[TextItem | FileItem]:
    """日記を取得し、テキストとファイルを時間順に並び替え

    Args:
        user_id (str): LINEユーザーID
        year (int): 日記の年
        month (int): 日記の月
        day (int): 日記の日
        print_diary (bool, optional): 日記を標準出力するかどうか. Defaults to False.

    Returns:
        list[TextItem | FileItem]: 日記のアイテム
    """
    """"""
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

    for item in [DiaryField.files.value, DiaryField.texts.value]:
        if item not in doc_dict:
            doc_dict[item] = {}
    files = doc_dict[DiaryField.files.value]
    texts = doc_dict[DiaryField.texts.value]

    file_list = convert_timestamps(files, FileField.timestamp.value)
    text_list = convert_timestamps(texts, TextField.timestamp.value)

    file_list = [FileItem(**item) for item in file_list]
    text_list = [TextItem(**item) for item in text_list]

    sorted_fields = sorted(
        file_list + text_list,
        key=lambda x: getattr(x, FileField.timestamp.value)
        if x in file_list
        else getattr(x, TextField.timestamp.value),
    )

    if print_diary:
        print(
            json.dumps(
                sorted_fields,
                indent=4,
                ensure_ascii=False,
                default=lambda x: x.isoformat() if isinstance(x, datetime) else x,
            )
        )
    return sorted_fields
