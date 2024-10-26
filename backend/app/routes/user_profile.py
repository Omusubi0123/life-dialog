from fastapi import APIRouter

from app.db.get_user import get_user_from_db
from app.schemas.user_schema import FetchProfile, User
from app.utils.data_enum import UserField

user_router = APIRouter()


@user_router.post("/user/fetch_profile", response_model=User)
def fetch_profile(fetch_diary: FetchProfile) -> User:
    """日記を取得しメッセージを時系列順に並び替えて返す"""
    user_dict = get_user_from_db(fetch_diary.user_id)

    user = User(**{field.value: user_dict.get(field.value) for field in UserField})
    return user
