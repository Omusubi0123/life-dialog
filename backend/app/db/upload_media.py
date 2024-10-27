import os

from app.gcp_settings import storage_client
from app.settings import settings
from app.utils.media_enum import MediaExtension, MediaType


def upload_media_to_gcs(
    file_name: str,
    file_data,
    media_type: str,
):
    """Google Cloud StorageにファイルをアップロードしてURLを返す

    Args:
        file_name (str): 保存先のファイル名
        file_data (_type_): LINEから送信されたファイルデータ
        media_type (str): 送信されたファイルのメディアタイプ

    Returns:
        _type_: アップロードされたファイルのURL
    """
    """"""
    extension = MediaExtension[MediaType(media_type).name].value

    bucket = storage_client.bucket(settings.gcs_bucket_name)
    blob = bucket.blob(os.path.join(media_type, f"{file_name}.{extension}"))

    blob.upload_from_string(file_data, content_type=f"{media_type}/{extension}")
    blob.make_public()
    print(f"File uploaded to {blob.public_url}")
    return blob.public_url
