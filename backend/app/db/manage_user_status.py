from app.db.session import session_scope
from app.models.user import User


def update_user_status(user_id: str, status: str):
    """DBのユーザーステータス(記録モード or 対話モード)を更新"""
    with session_scope() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        user.mode = status


def get_user_status(user_id: str):
    """DBのユーザーステータス(記録モード or 対話モード)を取得"""
    with session_scope() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        return user.mode
