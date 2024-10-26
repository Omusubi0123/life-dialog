import json
import os
from datetime import datetime
from typing import Any

from app.gcp_settings import db
from app.utils.data_enum import (
    DiaryCollection,
    DiaryField,
    FileField,
    RootCollection,
    TextField,
)
from app.utils.timestamp_format import firestore_timestamp_to_datetime


def sort_diary_field_timeorder(
    user_id: str, timestamp: datetime, print_diary: bool = False
):
    """日記を取得し、テキストとファイルを時間順に並び替え"""

    def convert_timestamps(
        fields: dict[str, Any], timestamp_field: str
    ) -> list[dict[str, Any]]:
        """タイムスタンプをdatetimeオブジェクトに変換するヘルパー関数"""
        result_list = []
        for item in fields.values():
            item[timestamp_field] = firestore_timestamp_to_datetime(
                item[timestamp_field]
            )
            result_list.append(item)
        return result_list

    day = timestamp.strftime("%Y-%m-%d")
    collection_name = os.path.join(
        RootCollection.diary.value, user_id, DiaryCollection.diary.value
    )
    doc_ref = db.collection(collection_name).document(day)
    doc = doc_ref.get()
    doc_dict = doc.to_dict()

    files = doc_dict[DiaryField.files.value]
    texts = doc_dict[DiaryField.texts.value]

    file_list = convert_timestamps(files, FileField.timestamp.value)
    text_list = convert_timestamps(texts, TextField.timestamp.value)

    sorted_fields = sorted(
        file_list + text_list,
        key=lambda x: x[FileField.timestamp.value]
        if x in file_list
        else x[TextField.timestamp.value],
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
