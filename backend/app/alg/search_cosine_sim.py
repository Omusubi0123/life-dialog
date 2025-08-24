from sqlalchemy import text

from app.alg.print_search_result import print_search_result
from app.db.session import session_scope
from app.utils.llm_response import get_embedding


def cosine_similar_diary(
    user_id: str, query: str, top_k: int = 4, debug: bool = False
) -> list[dict]:
    """指定したユーザーの日記の中から、クエリに最も類似した日記を取得"""
    with session_scope() as session:
        query_vector: list[float] = get_embedding(query)
        sql_query = text(
            f"""
            SELECT user_id, diary_id, date, diary_content, 1 - (diary_vector <-> '{query_vector}') AS similarity
            FROM diary_vector
            WHERE user_id = '{user_id}'
            ORDER BY similarity DESC
            LIMIT {top_k}
            """
        )

        results = session.execute(sql_query).fetchall()

        results = [
            {
                "user_id": row.user_id,
                "diary_id": row.diary_id,
                "date": row.date,
                "diary_content": row.diary_content,
                "score": row.similarity,
            }
            for row in results
        ]

        if debug:
            print_search_result(results, "semantic", 10)
        return results
