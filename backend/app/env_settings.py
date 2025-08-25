from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    channel_id: str
    channel_secret: str
    channel_access_token: str

    openai_api_key: str

    database_url: str

    elasticsearch_url: str
    elasticsearch_port: str
    elasticsearch_index: str

    nginx_file_url: str
    frontend_url: str

    google_client_id: str
    google_client_secret: str

    jwt_secret_key: str
    jwt_algorithm: str  # ex. "HS256"
    jwt_expire_minutes: int  # ex. 60 * 24 * 7  # 1週間

    model_config = {"env_file": ".env"}


env = EnvSettings()
