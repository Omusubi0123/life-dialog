"""
日記リポジトリ

日記とメッセージに関するデータベース操作をまとめる
"""

from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from app.models import Diary, DiaryVector, Message


class DiaryRepository:
    """日記のデータアクセス層"""

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, diary_id: int) -> Optional[Diary]:
        """日記IDで日記を取得"""
        return self.session.query(Diary).filter(Diary.diary_id == diary_id).first()

    def get_by_user_and_date(self, user_id: str, target_date: date) -> Optional[Diary]:
        """ユーザーIDと日付で日記を取得"""
        return (
            self.session.query(Diary)
            .filter(Diary.user_id == user_id, Diary.date == target_date)
            .first()
        )

    def get_or_create_by_user_and_date(self, user_id: str, target_date: date) -> Diary:
        """ユーザーIDと日付で日記を取得、なければ作成"""
        diary = self.get_by_user_and_date(user_id, target_date)
        if not diary:
            diary = self.create(user_id, target_date)
        return diary

    def create(
        self,
        user_id: str,
        target_date: date,
        title: str = None,
        summary: str = None,
        feedback: str = None,
    ) -> Diary:
        """新しい日記を作成"""
        diary = Diary(
            user_id=user_id,
            date=target_date,
            title=title,
            summary=summary,
            feedback=feedback,
        )
        self.session.add(diary)
        self.session.flush()
        return diary

    def update_summary(
        self, diary_id: int, title: str, summary: str, feedback: str
    ) -> Optional[Diary]:
        """日記のサマリーを更新"""
        diary = self.get_by_id(diary_id)
        if diary:
            diary.title = title
            diary.summary = summary
            diary.feedback = feedback
            self.session.flush()
        return diary

    def get_user_diaries(self, user_id: str, limit: int = None) -> list[Diary]:
        """ユーザーの日記一覧を取得"""
        query = (
            self.session.query(Diary)
            .filter(Diary.user_id == user_id)
            .order_by(Diary.date.desc())
        )
        if limit:
            query = query.limit(limit)
        return query.all()


class MessageRepository:
    """メッセージのデータアクセス層"""

    def __init__(self, session: Session):
        self.session = session

    def get_by_diary_id(self, diary_id: int) -> list[Message]:
        """日記IDでメッセージ一覧を取得"""
        return (
            self.session.query(Message)
            .filter(Message.diary_id == diary_id)
            .order_by(Message.sent_at)
            .all()
        )

    def get_by_user_and_date(self, user_id: str, target_date: date) -> list[Message]:
        """ユーザーIDと日付でメッセージ一覧を取得"""
        return (
            self.session.query(Message)
            .join(Diary)
            .filter(Message.user_id == user_id, Diary.date == target_date)
            .order_by(Message.sent_at)
            .all()
        )

    def create(
        self,
        diary_id: int,
        user_id: str,
        media_type: str,
        content: str,
    ) -> Message:
        """新しいメッセージを作成"""
        message = Message(
            diary_id=diary_id,
            user_id=user_id,
            media_type=media_type,
            content=content,
        )
        self.session.add(message)
        self.session.flush()
        return message


class DiaryVectorRepository:
    """日記ベクトルのデータアクセス層"""

    def __init__(self, session: Session):
        self.session = session

    def upsert(
        self,
        user_id: str,
        diary_id: int,
        target_date: date,
        diary_content: str,
        diary_vector: list[float],
    ) -> DiaryVector:
        """日記ベクトルを作成または更新"""
        # 既存のベクトルを確認
        existing = (
            self.session.query(DiaryVector)
            .filter(DiaryVector.diary_id == diary_id)
            .first()
        )

        if existing:
            # 更新
            existing.diary_content = diary_content
            existing.diary_vector = diary_vector
            self.session.flush()
            return existing
        else:
            # 新規作成
            vector = DiaryVector(
                user_id=user_id,
                diary_id=diary_id,
                date=target_date,
                diary_content=diary_content,
                diary_vector=diary_vector,
            )
            self.session.add(vector)
            self.session.flush()
            return vector
