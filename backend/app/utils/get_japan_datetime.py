from datetime import datetime

import pytz


def get_japan_timestamp() -> datetime:
    """日本時間の現在時刻を取得する"""
    timezone = pytz.timezone("Asia/Tokyo")
    return datetime.now(timezone)


def get_japan_date() -> datetime:
    """日本時間の現在日付を取得する"""
    return get_japan_timestamp().date()


def get_japan_time() -> datetime:
    """日本時間の現在時刻を取得する"""
    return get_japan_timestamp().time().replace(microsecond=0)
