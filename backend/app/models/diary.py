"""
日記関連のモデル
"""

from sqlalchemy import DATE, TIME, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.utils.get_japan_datetime import get_japan_date, get_japan_time

from .base import BaseClass


class Diary(BaseClass):
    """日記モデル"""

    __tablename__ = "diary"

    diary_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(40), ForeignKey("users.user_id"))
    date = Column(DATE, default=lambda: get_japan_date())
    title = Column(Text)
    summary = Column(Text)
    feedback = Column(Text)

    # リレーションシップ
    user = relationship("User", back_populates="diaries")
    messages = relationship("Message", back_populates="diary")
    diary_vector = relationship("DiaryVector", back_populates="diary")


class Message(BaseClass):
    """メッセージモデル"""

    __tablename__ = "message"

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    diary_id = Column(Integer, ForeignKey("diary.diary_id"))
    user_id = Column(String(40), ForeignKey("users.user_id"))
    media_type = Column(String(10))
    content = Column(Text)
    sent_at = Column(TIME, default=lambda: get_japan_time())

    # リレーションシップ
    diary = relationship("Diary", back_populates="messages")
