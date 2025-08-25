from app.alg.analyze_user import analyze_user_by_llm
from app.db.repositories.analysis import AnalysisRepository
from app.db.session import session_scope
from app.utils.get_japan_datetime import get_japan_time


def set_user_analysis(user_id: str) -> dict:
    """ユーザーの分析を生成・DBに追加し、既に存在する場合は更新する"""
    personality, strength, weakness = analyze_user_by_llm(user_id)
    with session_scope() as session:
        analysis_repo = AnalysisRepository(session)
        new_analysis = analysis_repo.upsert(user_id, personality, strength, weakness)
        print(f"User analysis added!! Time:", get_japan_time(), flush=True)
        return new_analysis.to_dict()
