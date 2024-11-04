import random
from datetime import date

from linebot.models import FlexSendMessage

from app.db.get_diary import get_date_diary
from app.db.get_message import get_date_message
from app.settings import settings
from app.utils.data_enum import QuickReplyField


def get_diary_random_image(user_id: str, date: date) -> str | None:
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
    messages = get_date_message(user_id, date)

    if any([message["media_type"] == "image" for message in messages]):
        # 'mediatype'が'image'のものだけを抽出
        image_files = [
            message["content"]
            for message in messages
            if message["media_type"] == "image"
        ]

        if image_files:
            return random.choice(image_files)
        else:
            return None
    else:
        return None


def create_flex_message(
    event, status: str, summary: str, date: date, date_list, user_id_list
):
    """日記をLINEで表示するためのflex messageを作成"""
    thumbnail_image_url = get_diary_random_image(event.source.user_id, date)
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
                            else f"{settings.nginx_file_url}/material/default_diary_thumbnail.jpg",
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
            diary = get_date_diary(user_id, date)

            if diary and diary["summary"]:
                cards_data.append(
                    {
                        "date": diary["date"],
                        "summary": diary["summary"],
                        "thumbnail_image_url": get_diary_random_image(user_id, date),
                    },
                )

        bubbles = []
        for card in cards_data:
            bubble = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": card["thumbnail_image_url"]
                    or f"{settings.nginx_file_url}/material/default_diary_thumbnail.jpg",
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
                                "uri": f"{settings.frontend_url}?date={card['date'][:4]}{card['date'][5:7]}{card['date'][8:]}&user_id={event.source.user_id}&",
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
