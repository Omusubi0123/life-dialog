from fastapi import APIRouter

from app.db.get_analysis import get_user_analysis
from app.db.get_user import get_user_profile
from app.schemas.user_schema import FetchProfile, UserProfile

user_router = APIRouter()


@user_router.post("/user/fetch_profile", response_model=UserProfile)
def fetch_profile(fetch_diary: FetchProfile) -> UserProfile:
    """日記を取得しメッセージを時系列順に並び替えて返す"""
    user_dict = get_user_profile(fetch_diary.user_id)
    user_profile = UserProfile(**user_dict)

    analysis = get_user_analysis(fetch_diary.user_id)
    if analysis:
        user_profile.personality = analysis.get("personality")
        user_profile.strength = analysis.get("strength")
        user_profile.weakness = analysis.get("weakness")

    return user_profile
