"""
認証関連のスキーマ
"""

from typing import Optional

from pydantic import BaseModel


class GoogleAuthCallbackRequest(BaseModel):
    """Google認証コールバックリクエスト"""

    code: str
    state: Optional[str] = None


class GoogleAuthCallbackResponse(BaseModel):
    """Google認証コールバックレスポンス"""

    access_token: str
    user_info: dict
    requires_link: bool = False


class LinkLineUserRequest(BaseModel):
    """LINE ユーザー紐付けリクエスト"""

    line_user_id: str


class LinkLineUserResponse(BaseModel):
    """LINE ユーザー紐付けレスポンス"""

    success: bool
    access_token: str


class UserInfoResponse(BaseModel):
    """ユーザー情報レスポンス"""

    google_id: str
    email: str
    name: str
    picture: Optional[str] = None
    line_user_id: Optional[str] = None
    has_line_link: bool


class AuthStatusResponse(BaseModel):
    """認証状態レスポンス"""

    is_authenticated: bool
    requires_line_link: bool = False
    user_info: Optional[UserInfoResponse] = None


class TokenLinkRequest(BaseModel):
    """トークンベース紐付けリクエスト"""
    token: str


class TokenLinkResponse(BaseModel):
    """トークンベース紐付けレスポンス"""
    success: bool
    access_token: str
    message: str
