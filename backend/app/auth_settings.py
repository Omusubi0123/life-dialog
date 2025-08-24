"""
認証関連の設定
"""

from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):
    """認証設定"""

    # Google OAuth設定
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    # JWT設定
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7  # 1週間

    # CORS設定
    frontend_url: str

    class Config:
        env_file = ".env"


# 設定インスタンス
auth_settings = AuthSettings()
