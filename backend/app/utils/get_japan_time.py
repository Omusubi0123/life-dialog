from datetime import datetime

import pytz


def get_japan_time() -> datetime:
    """日本時間の現在時刻を取得する"""
    return datetime.now(pytz.timezone("Asia/Tokyo"))
