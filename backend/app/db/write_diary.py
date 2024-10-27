import os
import uuid

from app.db.upload_media import upload_media_to_gcs
from app.gcp_settings import db
from app.utils.data_enum import (
    DiaryCollection,
    DiaryField,
    FileField,
    RootCollection,
    TextField,
)
from app.utils.media_enum import MediaType
from app.utils.timestamp_format import timestamp_md_to_datetime


def update_doc_field(
    user_id: str,
    message_id: str,
    data: str,
    mediatype: MediaType,
    timestamp: str,
) -> str:
    """日記ドキュメントにテキストまたはファイルURLを追加

    Args:
        user_id (str): LINEユーザーID
        message_id (str): 送信されたLINEメッセージのID
        data (str): テキストまたはファイルURL
        mediatype (MediaType): メディアの種類
        timestamp (str): 送信されたLINEメッセージのタイムスタンプ

    Returns:
        str: テキストまたはファイルURL
    """
    """"""
    timestamp = timestamp_md_to_datetime(timestamp)
    today = timestamp.strftime("%Y-%m-%d")

    collection_name = os.path.join(
        RootCollection.diary.value, user_id, DiaryCollection.diary.value
    )

    doc_ref = db.collection(collection_name).document(today)
    doc = doc_ref.get()

    url = ""
    if mediatype == MediaType.TEXT.value:
        field_type = DiaryField.texts.value
        doc_data = {
            DiaryField.texts.value: {
                message_id: {
                    TextField.text.value: data,
                    TextField.timestamp.value: timestamp,
                },
            },
        }
    else:
        field_type = DiaryField.files.value
        url = upload_media_to_gcs(f"{user_id}_{timestamp}", data.content, mediatype)
        doc_data = {
            DiaryField.files.value: {
                message_id: {
                    FileField.url.value: url,
                    FileField.mediatype.value: mediatype,
                    FileField.timestamp.value: timestamp,
                },
            },
        }

    if doc.exists:
        doc_dict = doc.to_dict()
        if field_type in doc_dict:
            doc_dict[DiaryField[field_type].value].update(
                doc_data[DiaryField[field_type].value]
            )
        else:
            doc_dict.update(doc_data)
        doc_ref.update(doc_dict)
        print(f"Document updated: {doc_dict}")
    else:
        # 今日の日記が存在しない場合は新規作成
        random_id = str(uuid.uuid4())
        doc_data[DiaryField.diary_id.value] = random_id
        doc_data[DiaryField.date.value] = today
        doc_ref.set(doc_data)
        print(f"Document created: {doc_data}")
    return data if mediatype == MediaType.TEXT.value else url
