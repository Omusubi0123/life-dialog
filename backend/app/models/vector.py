"""
ベクトル関連のモデル
"""

from pgvector.sqlalchemy import Vector
from sqlalchemy import DATE, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import BaseClass


class DiaryVector(BaseClass):
    """日記ベクトルモデル"""

    __tablename__ = "diary_vector"

    vector_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(40), ForeignKey("users.user_id"))
    diary_id = Column(Integer, ForeignKey("diary.diary_id"))
    date = Column(DATE)
    diary_content = Column(Text)
    diary_vector = Column(Vector(1536))

    # リレーションシップ
    diary = relationship("Diary", back_populates="diary_vector")
