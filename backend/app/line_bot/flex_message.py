import random

from linebot.models import FlexSendMessage

from app.db.get_diary import get_diary_from_db
from app.settings import settings
from app.utils.data_enum import QuickReplyField


def get_diary_random_image(user_id, year, month, day):
    """選択された日記からランダムに画像を取得"""
    doc_dict = get_diary_from_db(user_id, year, month, day)
    if (
        "files" in doc_dict
        and isinstance(doc_dict["files"], dict)
        and len(doc_dict["files"]) > 0
    ):
        # 'mediatype'が'image'のものだけを抽出
        image_files = [
            file_data["url"]
            for file_data in doc_dict["files"].values()
            if file_data["mediatype"] == "image"
        ]

        if image_files:
            return random.choice(image_files)
        else:
            return None
    else:
        return None


def create_flex_message(event, status, summary, year, month, day):
    """日記をLINEで表示するためのflex messageを作成"""
    print(f"えええ")
    thumbnail_image_url = get_diary_random_image(event.source.user_id, year, month, day)
    print(thumbnail_image_url)
    print(f"ううう")

    if event.message.text == QuickReplyField.view_diary.value:
        flex_message = FlexSendMessage(
            alt_text="複数のカードメッセージ",
            contents={
                "type": "carousel",
                "contents": [
                    {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": thumbnail_image_url
                            if thumbnail_image_url
                            else "https://firebasestorage.googleapis.com/v0/b/jp-hacks-77212.appspot.com/o/material%2Fdefault_diary_thumbnail.jpg?alt=media&token=9aad0b1e-04e4-4727-97a6-2668de248d02",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "今日の日記",
                                    "weight": "bold",
                                    "size": "xl",
                                },
                                {
                                    "type": "text",
                                    "text": f"{summary[:47]}...",
                                    "size": "md",
                                    "wrap": True,
                                },
                            ],
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "uri",
                                        "label": "この日記を見る",
                                        "uri": f"{settings.frontend_url}?user_id={event.source.user_id}",
                                    },
                                }
                            ],
                        },
                    },
                ],
            },
        )
    elif status == QuickReplyField.interactive_mode.value:
        # TODO: 日記検索の場合は、探した日記をリンク付きで送信するのでflex_messageを作る必要がある
        flex_message = None
    else:
        flex_message = None
    return flex_message
