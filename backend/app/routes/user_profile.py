from fastapi import APIRouter

from app.db.get_user import get_user_from_db
from app.schemas.user_schema import FetchProfile, User

user_router = APIRouter()


@user_router.post("/user/fetch_profile", response_model=User)
def fetch_profile(fetch_diary: FetchProfile) -> User:
    """日記を取得しメッセージを時系列順に並び替えて返す"""
    user_dict = get_user_from_db(fetch_diary.user_id)

    user = User(
        user_id=user_dict.get("user_id"),
        linkToken=user_dict.get("linkToken"),
        user_name=user_dict.get("user_name", ""),
        icon_url=user_dict.get("icon_url", ""),
        status_message=user_dict.get("status_message", ""),
        created_at=user_dict.get("created_at", "2024-01-01"),
        updated_at=user_dict.get("updated_at", "2024-01-01"),
        personality=user_dict.get("personality", ""),
        strength=user_dict.get("strength", ""),
        weakness=user_dict.get("weakness", ""),
    )

    return user
