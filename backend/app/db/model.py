from sqlalchemy import DATE, TIMESTAMP, Column, ForeignKey, Integer, String, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    mode = Column(String(10))
    icon_url = Column(Text)
    status_message = Column(Text)
    link_token = Column(Text)

    analyses = relationship("Analysis", back_populates="user")
    diaries = relationship("Diary", back_populates="user")


class Analysis(Base):
    __tablename__ = "analysis"

    analysis_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    uploaded_at = Column(TIMESTAMP, server_default=func.now())
    personality = Column(Text)
    strength = Column(Text)
    weakness = Column(Text)

    user = relationship("User", back_populates="analyses")


class Diary(Base):
    __tablename__ = "diary"

    diary_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    date = Column(DATE)
    title = Column(Text)
    summary = Column(Text)
    feedback = Column(Text)

    user = relationship("User", back_populates="diaries")
    messages = relationship("Message", back_populates="diary")


class Message(Base):
    __tablename__ = "message"

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    diary_id = Column(Integer, ForeignKey("diary.diary_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    media_type = Column(String(10))
    content = Column(Text)
    sent_at = Column(TIMESTAMP, server_default=func.now())

    diary = relationship("Diary", back_populates="messages")
