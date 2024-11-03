from sqlalchemy import DATE, TIME, TIMESTAMP, Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.utils.get_japan_datetime import (
    get_japan_date,
    get_japan_time,
    get_japan_timestamp,
)

Base = declarative_base()


class User(Base):
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

    analyses = relationship("Analysis", back_populates="user")
    diaries = relationship("Diary", back_populates="user")


class Analysis(Base):
    __tablename__ = "analysis"

    analysis_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(40), ForeignKey("users.user_id"))
    uploaded_at = Column(
        TIMESTAMP(timezone=True), default=lambda: get_japan_timestamp()
    )
    personality = Column(Text)
    strength = Column(Text)
    weakness = Column(Text)

    user = relationship("User", back_populates="analyses")


class Diary(Base):
    __tablename__ = "diary"

    diary_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(40), ForeignKey("users.user_id"))
    date = Column(DATE, default=lambda: get_japan_date())
    title = Column(Text)
    content = Column(Text)
    summary = Column(Text)
    feedback = Column(Text)

    user = relationship("User", back_populates="diaries")
    messages = relationship("Message", back_populates="diary")


class Message(Base):
    __tablename__ = "message"

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    diary_id = Column(Integer, ForeignKey("diary.diary_id"))
    user_id = Column(String(40), ForeignKey("users.user_id"))
    media_type = Column(String(10))
    content = Column(Text)
    sent_at = Column(TIME, default=lambda: get_japan_time())

    diary = relationship("Diary", back_populates="messages")
