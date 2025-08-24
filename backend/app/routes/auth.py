"""
認証関連のルート
"""

import secrets
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth_settings import auth_settings
from app.db.repositories.auth import GoogleUserRepository, UserGoogleLinkRepository
from app.db.repositories.user import UserRepository
from app.db.session import session_scope
from app.schemas.auth_schema import (
    AuthStatusResponse,
    GoogleAuthCallbackRequest,
    GoogleAuthCallbackResponse,
    LinkLineUserRequest,
    LinkLineUserResponse,
    UserInfoResponse,
)
from app.utils.auth import AuthenticatedUser, create_access_token, get_current_user

auth_router = APIRouter()


@auth_router.get("/auth/google/login")
def google_login():
    """Google OAuth 認証開始"""
    # PKCEのcode_verifierとcode_challengeを生成
    code_verifier = secrets.token_urlsafe(32)

    # Googleの認証URL作成
    params = {
        "client_id": auth_settings.google_client_id,
        "redirect_uri": auth_settings.google_redirect_uri,
        "scope": "openid email profile",
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
        "state": code_verifier,  # CSRF保護のためstateを使用
    }

    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"

    return {"auth_url": auth_url, "code_verifier": code_verifier}


@auth_router.post("/auth/google/callback", response_model=GoogleAuthCallbackResponse)
async def google_callback(request: GoogleAuthCallbackRequest):
    """Google OAuth コールバック処理"""
    try:
        # アクセストークンを取得
        token_data = {
            "client_id": auth_settings.google_client_id,
            "client_secret": auth_settings.google_client_secret,
            "code": request.code,
            "grant_type": "authorization_code",
            "redirect_uri": auth_settings.google_redirect_uri,
        }

        async with httpx.AsyncClient() as client:
            # Googleからアクセストークンを取得
            token_response = await client.post(
                "https://oauth2.googleapis.com/token", data=token_data
            )
            token_response.raise_for_status()
            token_info = token_response.json()

            # ユーザー情報を取得
            user_response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {token_info['access_token']}"},
            )
            user_response.raise_for_status()
            user_info = user_response.json()

        # データベースにユーザー情報を保存
        with session_scope() as session:
            google_user_repo = GoogleUserRepository(session)
            user_link_repo = UserGoogleLinkRepository(session)

            google_user = google_user_repo.get_by_id(user_info["id"])
            if not google_user:
                # 新規ユーザーを作成
                google_user = google_user_repo.create(
                    google_id=user_info["id"],
                    email=user_info["email"],
                    name=user_info.get("name", ""),
                    picture=user_info.get("picture", ""),
                )
            else:
                # 既存ユーザーの情報を更新
                google_user = google_user_repo.update(
                    google_user,
                    name=user_info.get("name", ""),
                    picture=user_info.get("picture", ""),
                )

            # LINE ユーザーとの紐付けを確認
            user_link = user_link_repo.get_by_google_id(user_info["id"])
            requires_link = user_link is None

            # JWTトークンを作成
            token_payload = {
                "sub": user_info["id"],
                "email": user_info["email"],
                "line_user_id": user_link.line_user_id if user_link else None,
            }
            access_token = create_access_token(token_payload)

            return GoogleAuthCallbackResponse(
                access_token=access_token,
                user_info=user_info,
                requires_link=requires_link,
            )

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google OAuth error: {e.response.text}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}",
        )


@auth_router.post("/auth/link-line-user", response_model=LinkLineUserResponse)
def link_line_user(
    request: LinkLineUserRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    """LINE ユーザーIDとの紐付け"""
    with session_scope() as session:
        user_repo = UserRepository(session)
        user_link_repo = UserGoogleLinkRepository(session)

        # LINE ユーザーが存在するか確認
        line_user = user_repo.get_by_id(request.line_user_id)
        if not line_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="LINE user not found"
            )

        # 既存の紐付けを確認
        existing_link = user_link_repo.get_by_line_user_id(request.line_user_id)
        if existing_link:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This LINE user is already linked to another Google account",
            )

        # Google ユーザーの既存紐付けを削除（あれば）
        user_link_repo.delete_by_google_id(current_user.google_id)

        # 新しい紐付けを作成
        user_link_repo.create(
            line_user_id=request.line_user_id, google_id=current_user.google_id
        )

        # 新しいJWTトークンを発行（LINE user_id付き）
        token_payload = {
            "sub": current_user.google_id,
            "email": current_user.email,
            "line_user_id": request.line_user_id,
        }
        access_token = create_access_token(token_payload)

        return LinkLineUserResponse(success=True, access_token=access_token)


@auth_router.get("/auth/me", response_model=UserInfoResponse)
def get_current_user_info(current_user: AuthenticatedUser = Depends(get_current_user)):
    """現在のユーザー情報を取得"""
    with session_scope() as session:
        google_user_repo = GoogleUserRepository(session)
        google_user = google_user_repo.get_by_id(current_user.google_id)

        return UserInfoResponse(
            google_id=current_user.google_id,
            email=current_user.email,
            name=current_user.name,
            picture=google_user.picture if google_user else None,
            line_user_id=current_user.line_user_id,
            has_line_link=current_user.line_user_id is not None,
        )


@auth_router.get("/auth/status", response_model=AuthStatusResponse)
def get_auth_status(current_user: AuthenticatedUser = Depends(get_current_user)):
    """認証状態を取得"""
    requires_line_link = current_user.line_user_id is None

    user_info = UserInfoResponse(
        google_id=current_user.google_id,
        email=current_user.email,
        name=current_user.name,
        line_user_id=current_user.line_user_id,
        has_line_link=not requires_line_link,
    )

    return AuthStatusResponse(
        is_authenticated=True,
        requires_line_link=requires_line_link,
        user_info=user_info,
    )
