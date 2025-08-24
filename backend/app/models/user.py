"""
ユーザー関連のモデル
"""

from sqlalchemy import TIMESTAMP, Column, String, Text
from sqlalchemy.orm import relationship

from app.utils.get_japan_datetime import get_japan_timestamp

from .base import BaseClass


class User(BaseClass):
    """ユーザーモデル"""

    __tablename__ = "users"

    user_id = Column(String(40), primary_key=True)
    name = Column(String(40))
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: get_japan_timestamp())
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: get_japan_timestamp(),
        onupdate=lambda: get_japan_timestamp(),
    )
    mode = Column(String(10))
    icon_url = Column(Text)
    status_message = Column(Text)
    link_token = Column(Text)

    # リレーションシップ
    analyses = relationship("Analysis", back_populates="user")
    diaries = relationship("Diary", back_populates="user")
