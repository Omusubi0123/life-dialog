from sqlalchemy import text

from app.utils.llm_response import get_embedding
from app.utils.session_scope import get_session


def cosine_similar_diary(user_id: str, query: str, top_k: int = 4) -> list[dict]:
    query_vector = get_embedding(query)
    sql_query = text(
        """
        SELECT user_id, diary_id, date, diary_content, 1 - (diary_vector <=> :query_vector) AS similarity
        FROM diary_vector
        WHERE user_id = :user_id
        ORDER BY similarity DESC
        LILMIT :top_k
    """
    )
    with get_session() as session:
        results = session.execute(
            sql_query,
            {"query_vector": query_vector, "top_k": top_k, "user_id": user_id},
        )
        return [
            {
                "user_id": row.user_id,
                "diary_id": row.diary_id,
                "date": row.date,
                "diary_content": row.diary_content,
                "score": row.similarity,
            }
            for row in results
        ]
