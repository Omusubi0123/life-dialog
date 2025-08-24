"""
ユーザーリポジトリ

ユーザーに関するデータベース操作をまとめる
"""

from typing import Optional

from sqlalchemy import update
from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    """ユーザーのデータアクセス層"""

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: str) -> Optional[User]:
        """ユーザーIDでユーザーを取得"""
        return self.session.query(User).filter(User.user_id == user_id).first()

    def get_all(self) -> list[User]:
        """全ユーザーを取得"""
        return self.session.query(User).all()

    def create(
        self,
        user_id: str,
        name: str,
        mode: str = None,
        icon_url: str = None,
        status_message: str = None,
        link_token: str = None,
    ) -> User:
        """新しいユーザーを作成"""
        user = User(
            user_id=user_id,
            name=name,
            mode=mode,
            icon_url=icon_url,
            status_message=status_message,
            link_token=link_token,
        )
        self.session.add(user)
        self.session.flush()
        return user

    def upsert(
        self,
        user_id: str,
        name: str,
        mode: str = None,
        icon_url: str = None,
        status_message: str = None,
        link_token: str = None,
    ) -> User:
        """ユーザーを作成または更新"""
        stmt = (
            update(User)
            .where(User.user_id == user_id)
            .values(
                name=name,
                mode=mode,
                icon_url=icon_url,
                status_message=status_message,
                link_token=link_token,
            )
        )
        result = self.session.execute(stmt)

        if result.rowcount == 0:
            # 更新された行がない場合は新規作成
            return self.create(
                user_id, name, mode, icon_url, status_message, link_token
            )
        else:
            # 更新が成功した場合は更新されたユーザーを取得
            self.session.flush()
            return self.get_by_id(user_id)

    def update_status(self, user_id: str, status: str) -> Optional[User]:
        """ユーザーのステータスを更新"""
        user = self.get_by_id(user_id)
        if user:
            user.mode = status
            self.session.flush()
        return user

    def delete(self, user_id: str) -> bool:
        """ユーザーを削除"""
        user = self.get_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.flush()
            return True
        return False
