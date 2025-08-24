"""
データベースセッション管理

セッションの作成、依存性注入、コンテキスト管理を行う
"""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.env_settings import env

# エンジンとセッションファクトリーを作成
engine = create_engine(env.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI依存性注入用のデータベースセッション生成関数

    Usage:
        @app.get("/users/")
        def get_users(db: Session = Depends(get_db)):
            return user_service.get_all_users(db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """
    セッションコンテキストマネージャー

    自動的にcommit/rollbackを管理する

    Usage:
        with session_scope() as session:
            user = User(name="test")
            session.add(user)
            # 自動的にcommitされる
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session() -> Session:
    """
    単純なセッション取得（手動でcommit/closeが必要）

    注意: 使用後は必ずsession.close()を呼ぶこと
    """
    return SessionLocal()
