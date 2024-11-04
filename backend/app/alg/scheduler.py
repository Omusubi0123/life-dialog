# Execute diary summary and embedding every day at 23:55
import time
from datetime import date

import schedule

from app.db.get_diary import get_date_diary
from app.db.get_user import get_user_names
from app.db.set_diary_summary import set_diary_summary
from app.db.set_diary_vector import set_diary_vector
from app.db.set_user_analysis import set_user_analysis


def register_diary(user_id: str, date: date):
    """dateの日記が空でなければ日記のベクトルと要約を生成する"""
    diary = get_date_diary(user_id, date)
    if diary:
        set_diary_summary(user_id, diary["diary_id"])
        set_diary_vector(user_id, date)
        set_user_analysis(user_id)


def scheduler_func():
    """全ユーザーの日記のベクトルと要約を生成する"""
    today = date.today()
    user_names = get_user_names()
    for user_name in user_names:
        register_diary(user_name, today)


schedule.every().day.at("23:55").do(scheduler_func)

while True:
    schedule.run_pending()
    time.sleep(60)
