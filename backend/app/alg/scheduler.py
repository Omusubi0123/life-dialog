# Execute diary summary and embedding every day at 23:55
import time
from datetime import date

import schedule

from app.db.get_diary import get_date_diary
from app.db.model import User
from app.db.set_diary_summary import set_diary_summary
from app.db.set_diary_vector import set_diary_vector
from app.utils.session_scope import get_session


def get_user_names():
    """DBに登録された全ユーザーのユーザーIDを取得する"""
    with get_session() as session:
        user_names = session.query(User.user_id).all()
        return [user_name[0] for user_name in user_names]


def register_diary(user_id: str, date: date):
    """dateの日記が空でなければ日記のベクトルと要約を生成する"""
    diary = get_date_diary(user_id, date)
    if diary:
        set_diary_vector(user_id, date)
        set_diary_summary(user_id, diary["diary_id"])


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
