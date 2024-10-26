from app.db.manage_user_status import get_user_status
from app.utils.data_enum import QuickReplyField


def get_current_status(event):
    """現在のステータス(記録モード or 対話モード)を取得"""
    if event.message.text == QuickReplyField.diary_mode.value:
        return QuickReplyField.diary_mode.value
    elif event.message.text == QuickReplyField.interactive_mode.value:
        return QuickReplyField.interactive_mode.value
    else:
        return get_user_status(event.source.user_id)
