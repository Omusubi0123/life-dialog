from app.db.model import User
from app.utils.session_scope import get_session


def get_user_profile(user_id: str) -> dict:
    """DBからユーザーのプロフィールを取得

    Args:
        user_id (str): LINEユーザーID

    Returns:
        User: ユーザーのプロフィール
    """
    with get_session() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        return user.to_dict() if user else None


def get_user_names():
    """DBに登録された全ユーザーのユーザーIDを取得する"""
    with get_session() as session:
        user_names = session.query(User.user_id).all()
        return [user_name[0] for user_name in user_names]
