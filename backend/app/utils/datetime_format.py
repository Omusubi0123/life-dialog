from datetime import datetime


def get_YMD_from_datetime(dt: datetime) -> tuple[int, int, int]:
    return dt.year, dt.month, dt.day

def get_HMS_from_datetime(dt: datetime) -> tuple[int, int, int]:
    return dt.hour, dt.minute, dt.second
