import random

from linebot.models import FlexSendMessage

from app.db.get_diary import get_diary_from_db
from app.settings import settings
from app.utils.data_enum import QuickReplyField


def get_diary_random_image(user_id: str, year: int, month: int, day: int) -> str | None:
    """選択された日記からランダムに画像を取得

    Args:
        user_id (str): LINEユーザーID
        year (int): 日記の年
        month (int): 日記の月
        day (int): 日記の日

    Returns:
        str | None: 画像URL
    """
    """"""
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


def create_flex_message(
    event, status, summary, year, month, day, date_list, user_id_list
):
    """日記をLINEで表示するためのflex messageを作成"""
    thumbnail_image_url = get_diary_random_image(event.source.user_id, year, month, day)
    print(thumbnail_image_url)

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
    elif (
        status == QuickReplyField.interactive_mode.value and date_list and user_id_list
    ):
        cards_data = []
        for date, user_id in zip(date_list, user_id_list):
            year, month, day = map(int, date.split("-"))
            diary_data = get_diary_from_db(user_id, year, month, day)
            if "summary" in diary_data and "date" in diary_data:
                cards_data.append(
                    {
                        "date": diary_data["date"],
                        "summary": diary_data["summary"],
                        "thumbnail_image_url": get_diary_random_image(
                            user_id, year, month, day
                        ),
                    },
                )

        bubbles = []
        for card in cards_data:
            bubble = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": card["thumbnail_image_url"]
                    or "https://firebasestorage.googleapis.com/v0/b/jp-hacks-77212.appspot.com/o/material%2Fdefault_diary_thumbnail.jpg?alt=media&token=9aad0b1e-04e4-4727-97a6-2668de248d02",
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
                            "text": card["date"],
                            "weight": "bold",
                            "size": "xl",
                        },
                        {
                            "type": "text",
                            "text": f"{card['summary'][:47]}...",
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
                                "uri": f"https://your-frontend-url.com?user_id=sample_user_id",
                            },
                        }
                    ],
                },
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(
            alt_text="複数のカードメッセージ",
            contents={
                "type": "carousel",
                "contents": bubbles,
            },
        )
    else:
        flex_message = None

    if flex_message is None or (flex_message.contents.contents == []):
        flex_message = FlexSendMessage(
            alt_text="日記がない通知",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "日記がないよ！",
                            "weight": "bold",
                            "size": "xl",
                        },
                        {
                            "type": "text",
                            "text": "「今日の日記」を押して日記を確認しよう",
                            "size": "md",
                            "wrap": True,
                        },
                    ],
                },
            },
        )
    return flex_message
