from app.elasticsearch_settings import es
from app.settings import settings

def save_diary_to_elasticsearch(diary: dict):
    """日記をElasticsearchに保存

    Args:
        diary (dict): 保存する日記の情報を含む辞書。キーは以下の通り。
            - diary_id (str): 日記のID
            - user_id (str): ユーザーのID
            - date (str): 日記の日付
            - diary_content (str): 日記の内容
    """
    assert all(key in diary for key in ["diary_id", "user_id", "date", "diary_content"]), "Invalid diary format for Elasticsearch"
    
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
