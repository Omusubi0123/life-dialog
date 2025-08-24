from app.db.session import session_scope
from app.models.analysis import Analysis


def get_user_analysis(user_id: str) -> dict:
    """DBからユーザーの分析情報を取得

    Args:
        user_id (str): LINEユーザーID

    Returns:
        User: ユーザーのプロフィール
    """
    with session_scope() as session:
        analysis = session.query(Analysis).filter(Analysis.user_id == user_id).first()
        return analysis.to_dict() if analysis else None
