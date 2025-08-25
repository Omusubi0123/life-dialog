import random
from datetime import date

from linebot.models import FlexSendMessage

from app.db.repositories.diary import DiaryRepository, MessageRepository
from app.db.session import session_scope
from app.env_settings import env
from app.utils.data_enum import QuickReplyField


def get_diary_random_image(user_id: str, date: date) -> str | None:
    """選択された日記からランダムに画像を取得

    Args:
        user_id (str): LINEユーザーID
        date (date): 日記の日付

    Returns:
        str | None: 画像URL
    """
    with session_scope() as session:
        message_repo = MessageRepository(session)
        messages = message_repo.get_by_user_and_date(user_id, date)

        if any([message.media_type == "image" for message in messages]):
            # 'mediatype'が'image'のものだけを抽出
            image_files = [
                message.content for message in messages if message.media_type == "image"
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
                            "url": (
                                thumbnail_image_url
                                if thumbnail_image_url
                                else f"{env.nginx_file_url}/material/default_diary_thumbnail.jpg"
                            ),
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
                                        "uri": f"{env.frontend_url}",
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
        with session_scope() as session:
            diary_repo = DiaryRepository(session)
            for date, user_id in zip(date_list, user_id_list):
                diary = diary_repo.get_by_user_and_date(user_id, date)

                if diary and diary.summary:
                    cards_data.append(
                        {
                            "date": diary.date.strftime("%Y%m%d"),
                            "summary": diary.summary,
                            "thumbnail_image_url": get_diary_random_image(
                                user_id, date
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
                    or f"{env.nginx_file_url}/material/default_diary_thumbnail.jpg",
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
                                "uri": f"{env.frontend_url}?date={card['date']}",
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
