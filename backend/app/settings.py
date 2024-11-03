from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    channel_id: str
    channel_secret: str
    channel_access_token: str

    firebase_credential: str
    firebase_project_id: str
    gcs_bucket_name: str

    openai_api_key: str
    azure_ai_search_endpoint: str
    azure_ai_search_admin_key: str
    azure_ai_search_index_name: str

    database_url: str

    nginx_file_url: str
    frontend_url: str

    model_config = {"env_file": ".env"}


settings = Settings()
