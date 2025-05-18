from app.elasticsearch_settings import es
from app.settings import settings

def save_diary_and_syn(diary: dict):
    assert ["diary_id", "user_id", "date", "diary_content"] == list(diary.keys()), "Invalid diary format for Elasticsearch"
    es.index(
        index=settings.elasticsearch_index,
        id=diary["diary_id"],
        body={
            "user_id": diary["user_id"],
            "diary_id": diary["diary_id"],
            "date": diary["date"],
            "diary_content": diary["diary_content"],
        }
    )
