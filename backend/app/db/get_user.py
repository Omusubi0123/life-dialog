from app.db.model import User
from app.utils.session_scope import get_session


def get_user_from_db(user_id: str) -> User:
    """DBからユーザーのプロフィールを取得

    Args:
        user_id (str): LINEユーザーID

    Returns:
        User: ユーザーのプロフィール
    """
    with get_session() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
    return user
