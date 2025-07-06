from pydantic_settings import BaseSettings


class Settings(BaseSettings):
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

    model_config = {"env_file": ".env"}


settings = Settings()
