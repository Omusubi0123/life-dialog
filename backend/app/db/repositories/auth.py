"""
認証関連のリポジトリ
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.auth import GoogleUser, UserGoogleLink


class GoogleUserRepository:
    """Googleユーザーリポジトリ"""

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, google_id: str) -> Optional[GoogleUser]:
        """Google IDでユーザーを取得"""
        return (
            self.session.query(GoogleUser)
            .filter(GoogleUser.google_id == google_id)
            .first()
        )

    def get_by_email(self, email: str) -> Optional[GoogleUser]:
        """メールアドレスでユーザーを取得"""
        return self.session.query(GoogleUser).filter(GoogleUser.email == email).first()

    def create(
        self, google_id: str, email: str, name: str, picture: str = None
    ) -> GoogleUser:
        """Googleユーザーを作成"""
        google_user = GoogleUser(
            google_id=google_id, email=email, name=name, picture=picture
        )
        self.session.add(google_user)
        self.session.commit()
        self.session.refresh(google_user)
        return google_user

    def update(self, google_user: GoogleUser, **kwargs) -> GoogleUser:
        """Googleユーザー情報を更新"""
        for key, value in kwargs.items():
            if hasattr(google_user, key):
                setattr(google_user, key, value)
        self.session.commit()
        self.session.refresh(google_user)
        return google_user


class UserGoogleLinkRepository:
    """ユーザーGoogle紐付けリポジトリ"""

    def __init__(self, session: Session):
        self.session = session

    def get_by_google_id(self, google_id: str) -> Optional[UserGoogleLink]:
        """Google IDで紐付けを取得"""
        return (
            self.session.query(UserGoogleLink)
            .filter(UserGoogleLink.google_id == google_id)
            .first()
        )

    def get_by_line_user_id(self, line_user_id: str) -> Optional[UserGoogleLink]:
        """LINE user IDで紐付けを取得"""
        return (
            self.session.query(UserGoogleLink)
            .filter(UserGoogleLink.line_user_id == line_user_id)
            .first()
        )

    def create(self, line_user_id: str, google_id: str) -> UserGoogleLink:
        """ユーザー紐付けを作成"""
        link = UserGoogleLink(line_user_id=line_user_id, google_id=google_id)
        self.session.add(link)
        self.session.commit()
        self.session.refresh(link)
        return link

    def delete_by_google_id(self, google_id: str) -> bool:
        """Google IDで紐付けを削除"""
        link = self.get_by_google_id(google_id)
        if link:
            self.session.delete(link)
            self.session.commit()
            return True
        return False
