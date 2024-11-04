import os

from app.settings import settings
from app.utils.media_enum import MediaExtension, MediaType


def save_media(user_id: str, message_id: str, message_content, media_type: str) -> str:
    """送信されたメディアを保存し、nginxのURLを返す

    Args:
        user_id (str): _description_
        message_id (str): _description_
        message_content (_type_): _description_
        media_type (str): _description_

    Returns:
        str: _description_
    """
    nginx_save_dir = os.path.join("/usr/share/nginx/html/files", user_id, media_type)
    extension = MediaExtension[MediaType(media_type).name].value

    os.makedirs(nginx_save_dir, exist_ok=True)
    filename = f"{message_id}.{extension}"

    with open(os.path.join(nginx_save_dir, filename), "wb") as f:
        for chunk in message_content.iter_content():
            f.write(chunk)

    fileurl = os.path.join(settings.nginx_file_url, user_id, media_type, filename)
    return fileurl
