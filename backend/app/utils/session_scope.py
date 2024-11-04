# postgresアクセスのためのセッション管理を行う
from contextlib import contextmanager

from app.db.config import SessionLocal


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
