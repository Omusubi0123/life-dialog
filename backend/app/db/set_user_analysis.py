from app.alg.analyze_user import analyze_user_by_llm
from app.db.db_insert import add_analysis
from app.utils.session_scope import get_session


def set_user_analysis(user_id: str) -> dict:
    """ユーザーの分析を生成・DBに追加し、既に存在する場合は更新する"""
    personality, strength, weakness = analyze_user_by_llm(user_id)
    with get_session() as session:
        new_analysis = add_analysis(session, user_id, personality, strength, weakness)
        return new_analysis.to_dict()
