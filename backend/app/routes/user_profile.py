from fastapi import APIRouter

from app.db.repositories.analysis import AnalysisRepository
from app.db.repositories.user import UserRepository
from app.schemas.user_schema import FetchProfile, UserProfile
from app.utils.session_scope import get_session

user_router = APIRouter()


@user_router.post("/user/fetch_profile", response_model=UserProfile)
def fetch_profile(fetch_diary: FetchProfile) -> UserProfile:
    """ユーザープロフィールを取得する"""
    with get_session() as session:
        user_repo = UserRepository(session)
        analysis_repo = AnalysisRepository(session)

        user = user_repo.get_by_id(fetch_diary.user_id)
        if not user:
            raise ValueError(f"User not found: {fetch_diary.user_id}")

        user_profile = UserProfile(**user.to_dict())

        analysis = analysis_repo.get_latest_by_user_id(fetch_diary.user_id)
        if analysis:
            user_profile.personality = analysis.personality
            user_profile.strength = analysis.strength
            user_profile.weakness = analysis.weakness

        return user_profile
