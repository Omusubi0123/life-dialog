from app.db.model import DiaryVector
from app.elasticsearch_settings import es
from app.env_settings import env
from app.utils.session_scope import get_session


def sync_diary_to_elasticsearch():
    with get_session() as session:
        diaries = session.query(DiaryVector).all()
        for diary in diaries:
            es.index(
                index=env.elasticsearch_index,
                id=diary.diary_id,
                body={
                    "user_id": diary.user_id,
                    "diary_id": diary.diary_id,
                    "date": diary.date,
                    "diary_content": diary.diary_content,
                },
            )
