"""
認証関連のユーティリティ
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from app.auth_settings import auth_settings
from app.db.repositories.auth import GoogleUserRepository, UserGoogleLinkRepository
from app.db.session import session_scope


class TokenData(BaseModel):
    """JWTトークンのデータ"""

    google_id: str
    line_user_id: Optional[str] = None


class AuthenticatedUser(BaseModel):
    """認証済みユーザー情報"""

    google_id: str
    email: str
    name: str
    line_user_id: Optional[str] = None


# HTTPベアラー認証スキーム
security = HTTPBearer()


def create_access_token(data: dict) -> str:
    """JWTアクセストークンを作成"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=auth_settings.jwt_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, auth_settings.jwt_secret_key, algorithm=auth_settings.jwt_algorithm
    )
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """JWTトークンを検証してユーザー情報を取得"""
    try:
        payload = jwt.decode(
            token,
            auth_settings.jwt_secret_key,
            algorithms=[auth_settings.jwt_algorithm],
        )
        google_id: str = payload.get("sub")
        if google_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(
            google_id=google_id, line_user_id=payload.get("line_user_id")
        )
        return token_data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> AuthenticatedUser:
    """現在のユーザーを取得（認証必須）"""
    token_data = verify_token(credentials.credentials)

    with session_scope() as session:
        google_user_repo = GoogleUserRepository(session)
        user_link_repo = UserGoogleLinkRepository(session)

        google_user = google_user_repo.get_by_id(token_data.google_id)
        if not google_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # LINE user_idの紐付けを確認
        user_link = user_link_repo.get_by_google_id(token_data.google_id)
        line_user_id = user_link.line_user_id if user_link else None

        return AuthenticatedUser(
            google_id=google_user.google_id,
            email=google_user.email,
            name=google_user.name,
            line_user_id=line_user_id,
        )


def get_current_user_with_line_id(
    current_user: AuthenticatedUser = Depends(get_current_user),
) -> AuthenticatedUser:
    """LINE IDの紐付けが必要なエンドポイント用の認証"""
    if not current_user.line_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="LINE user ID link required. Please link your LINE account first.",
        )
    return current_user
