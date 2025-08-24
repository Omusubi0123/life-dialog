"""
分析関連のモデル
"""

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.utils.get_japan_datetime import get_japan_timestamp

from .base import BaseClass


class Analysis(BaseClass):
    """ユーザー分析モデル"""

    __tablename__ = "analysis"

    analysis_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(40), ForeignKey("users.user_id"))
    uploaded_at = Column(TIMESTAMP, default=lambda: get_japan_timestamp())
    personality = Column(Text)
    strength = Column(Text)
    weakness = Column(Text)

    # リレーションシップ
    user = relationship("User", back_populates="analyses")
