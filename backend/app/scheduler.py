# Execute diary summary and embedding every day
from datetime import date, datetime, timedelta

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.db.repositories.diary import DiaryRepository
from app.db.repositories.user import UserRepository
from app.db.session import session_scope
from app.db.set_diary_summary import set_diary_summary
from app.db.set_diary_vector import set_diary_vector
from app.db.set_user_analysis import set_user_analysis
from app.elastic.save_new_diary import save_diary_to_elasticsearch
from app.elastic.sync_diary import sync_diary_to_elasticsearch
from app.elastic.wait_for_es import wait_for_es

scheduler = AsyncIOScheduler()


def register_diary(user_id: str, date: date):
    """dateの日記が空でなければ日記のベクトルと要約を生成する"""
    with session_scope() as session:
        diary_repo = DiaryRepository(session)
        diary = diary_repo.get_by_user_and_date(user_id, date)
        if diary:
            set_diary_summary(user_id, diary.diary_id)
            new_diary = set_diary_vector(user_id, date)
            save_diary_to_elasticsearch(new_diary)
            set_user_analysis(user_id)


def scheduler_func():
    """全ユーザーの日記のベクトルと要約を生成する"""
    today = date.today()
    with session_scope() as session:
        user_repo = UserRepository(session)
        user_ids = [user.user_id for user in user_repo.get_all()]
        for user_id in user_ids:
            register_diary(user_id, today)


def get_jst_time_str(hour: int, minute: int) -> str:
    """日本時間での指定時刻をUTCに変換した文字列を返す"""
    jst = pytz.timezone("Asia/Tokyo")
    target_time = datetime.now(jst).replace(
        hour=hour, minute=minute, second=0, microsecond=0
    )
    utc_time = target_time.astimezone(pytz.utc)
    return utc_time.strftime("%H:%M")


scheduler.add_job(scheduler_func, "cron", hour=23, minute=55, timezone="Asia/Tokyo")

scheduler.add_job(
    lambda: (wait_for_es(), sync_diary_to_elasticsearch()),
    "date",
    run_date=datetime.now() + timedelta(seconds=10),
)


def start_scheduler():
    scheduler.start()
