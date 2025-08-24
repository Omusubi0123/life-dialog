"""
分析リポジトリ

ユーザー分析に関するデータベース操作をまとめる
"""

from typing import Optional

from sqlalchemy import update
from sqlalchemy.orm import Session

from app.models import Analysis


class AnalysisRepository:
    """分析のデータアクセス層"""

    def __init__(self, session: Session):
        self.session = session

    def get_by_user_id(self, user_id: str) -> Optional[Analysis]:
        """ユーザーIDで分析を取得"""
        return self.session.query(Analysis).filter(Analysis.user_id == user_id).first()

    def get_latest_by_user_id(self, user_id: str) -> Optional[Analysis]:
        """ユーザーIDで最新の分析を取得"""
        return (
            self.session.query(Analysis)
            .filter(Analysis.user_id == user_id)
            .order_by(Analysis.uploaded_at.desc())
            .first()
        )

    def create(
        self,
        user_id: str,
        personality: str,
        strength: str,
        weakness: str,
    ) -> Analysis:
        """新しい分析を作成"""
        analysis = Analysis(
            user_id=user_id,
            personality=personality,
            strength=strength,
            weakness=weakness,
        )
        self.session.add(analysis)
        self.session.flush()
        return analysis

    def upsert(
        self,
        user_id: str,
        personality: str,
        strength: str,
        weakness: str,
    ) -> Analysis:
        """分析を作成または更新"""
        stmt = (
            update(Analysis)
            .where(Analysis.user_id == user_id)
            .values(
                personality=personality,
                strength=strength,
                weakness=weakness,
            )
        )
        result = self.session.execute(stmt)

        if result.rowcount == 0:
            # 更新された行がない場合は新規作成
            return self.create(user_id, personality, strength, weakness)
        else:
            # 更新が成功した場合は更新された分析を取得
            self.session.flush()
            return self.get_by_user_id(user_id)

    def get_user_analyses(self, user_id: str, limit: int = None) -> list[Analysis]:
        """ユーザーの分析履歴を取得"""
        query = (
            self.session.query(Analysis)
            .filter(Analysis.user_id == user_id)
            .order_by(Analysis.uploaded_at.desc())
        )
        if limit:
            query = query.limit(limit)
        return query.all()
