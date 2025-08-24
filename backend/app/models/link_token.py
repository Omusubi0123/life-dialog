"""
アカウント紐付け用ワンタイムトークンモデル
"""

from datetime import datetime, timedelta
from sqlalchemy import TIMESTAMP, Column, String, Boolean
from app.utils.get_japan_datetime import get_japan_timestamp
from .base import BaseClass


class LinkToken(BaseClass):
    """アカウント紐付け用ワンタイムトークンモデル"""

    __tablename__ = "link_tokens"

    token = Column(String(64), primary_key=True)
    line_user_id = Column(String(40), nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: get_japan_timestamp())
    used_at = Column(TIMESTAMP(timezone=True), nullable=True)

    @classmethod
    def create_token(cls, line_user_id: str, expires_minutes: int = 30):
        """新しいリンクトークンを作成"""
        import secrets
        
        token = secrets.token_urlsafe(48)
        expires_at = get_japan_timestamp() + timedelta(minutes=expires_minutes)
        
        return cls(
            token=token,
            line_user_id=line_user_id,
            expires_at=expires_at
        )

    def is_valid(self) -> bool:
        """トークンが有効かどうかを確認"""
        now = get_japan_timestamp()
        return not self.is_used and self.expires_at > now

    def mark_as_used(self):
        """トークンを使用済みにマーク"""
        self.is_used = True
        self.used_at = get_japan_timestamp()
