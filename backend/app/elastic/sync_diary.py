from app.db.session import session_scope
from app.elasticsearch_settings import es
from app.env_settings import env
from app.models.vector import DiaryVector


def sync_diary_to_elasticsearch():
    with session_scope() as session:
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
