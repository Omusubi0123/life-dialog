from app.db.model import Analysis
from app.utils.session_scope import get_session


def get_user_analysis(user_id: str) -> dict:
    """DBからユーザーの分析情報を取得

    Args:
        user_id (str): LINEユーザーID

    Returns:
        User: ユーザーのプロフィール
    """
    with get_session() as session:
        analysis = session.query(Analysis).filter(Analysis.user_id == user_id).first()
        return analysis.to_dict() if analysis else None
