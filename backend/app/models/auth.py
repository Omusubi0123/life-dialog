"""
認証関連のモデル
"""

from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.utils.get_japan_datetime import get_japan_timestamp

from .base import BaseClass


class GoogleUser(BaseClass):
    """Googleユーザー情報モデル"""

    __tablename__ = "google_users"

    google_id = Column(String(100), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100))
    picture = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: get_japan_timestamp())
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: get_japan_timestamp(),
        onupdate=lambda: get_japan_timestamp(),
    )

    # リレーションシップ
    user_links = relationship("UserGoogleLink", back_populates="google_user")


class UserGoogleLink(BaseClass):
    """LINEユーザーとGoogleユーザーの紐付けモデル"""

    __tablename__ = "user_google_links"

    line_user_id = Column(String(40), ForeignKey("users.user_id"), primary_key=True)
    google_id = Column(
        String(100), ForeignKey("google_users.google_id"), primary_key=True
    )
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: get_japan_timestamp())

    # リレーションシップ
    user = relationship("User")
    google_user = relationship("GoogleUser", back_populates="user_links")
