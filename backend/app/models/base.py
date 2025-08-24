"""
ベースモデルの定義
"""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseClass(Base):
    """全モデルの基底クラス"""

    __abstract__ = True

    def to_dict(self) -> dict:
        """SQLAlchemyのモデルをdictに変換する"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
