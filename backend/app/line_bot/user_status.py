from app.db.repositories.user import UserRepository
from app.utils.data_enum import QuickReplyField
from app.utils.session_scope import get_session


def get_current_status(user_id, event):
    """現在のステータス(記録モード or 対話モード)を取得"""
    if event.message.text == QuickReplyField.diary_mode.value:
        return QuickReplyField.diary_mode.value
    elif event.message.text == QuickReplyField.interactive_mode.value:
        return QuickReplyField.interactive_mode.value
    else:
        with get_session() as session:
            user_repo = UserRepository(session)
            user = user_repo.get_by_id(user_id)
            return user.mode if user else None
