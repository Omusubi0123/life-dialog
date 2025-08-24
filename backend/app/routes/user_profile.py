from fastapi import APIRouter, Depends

from app.db.repositories.analysis import AnalysisRepository
from app.db.repositories.user import UserRepository
from app.db.session import session_scope
from app.schemas.user_schema import FetchProfile, UserProfile
from app.utils.auth import AuthenticatedUser, get_current_user_with_line_id

user_router = APIRouter()


@user_router.post("/user/fetch_profile", response_model=UserProfile)
def fetch_profile(
    fetch_diary: FetchProfile,
    current_user: AuthenticatedUser = Depends(get_current_user_with_line_id),
) -> UserProfile:
    """ユーザープロフィールを取得する（認証必須）"""
    # 認証されたユーザーのLINE IDを使用
    user_id = current_user.line_user_id

    with session_scope() as session:
        user_repo = UserRepository(session)
        analysis_repo = AnalysisRepository(session)

        user = user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User not found: {user_id}")

        user_profile = UserProfile(**user.to_dict())

        analysis = analysis_repo.get_latest_by_user_id(user_id)
        if analysis:
            user_profile.personality = analysis.personality
            user_profile.strength = analysis.strength
            user_profile.weakness = analysis.weakness

        return user_profile
