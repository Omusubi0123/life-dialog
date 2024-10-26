from datetime import datetime, timedelta, timezone


def timestamp_ms_to_s(timestamp: str) -> int:
    """LINE botのミリ秒単位のタイムスタンプを秒単位に変換する"""
    return int(timestamp) // 1000


def timestamp_ms_to_s_and_ns(timestamp: str) -> tuple[int, int]:
    """LINE botのミリ秒単位のタイムスタンプを秒単位とナノ秒単位に変換する"""
    seconds = int(timestamp) // 1000
    nanoseconds = int(timestamp) % 1000 * 1000000
    return seconds, nanoseconds


def timestamp_md_to_datetime(timestamp: str) -> datetime:
    """LINE botのミリ秒単位のタイムスタンプをdatetimeオブジェクトに変換する"""
    jst = timezone(timedelta(hours=+9), "JST")
    timestamp = datetime.fromtimestamp(timestamp_ms_to_s(timestamp), jst)
    return timestamp


def firestore_timestamp_to_datetime(timestamp) -> datetime:
    """Firestoreのタイムスタンプをdatetimeオブジェクトに変換する"""
    jst = timezone(timedelta(hours=+9), "JST")
    timestamp = timestamp.astimezone(jst)

    standard_datetime = datetime(
        timestamp.year,
        timestamp.month,
        timestamp.day,
        timestamp.hour,
        timestamp.minute,
        timestamp.second,
        timestamp.microsecond,
        tzinfo=timestamp.tzinfo,
    )
    return standard_datetime
