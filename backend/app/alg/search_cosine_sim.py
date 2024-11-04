from sqlalchemy import text

from app.utils.llm_response import get_embedding
from app.utils.session_scope import get_session


def search_similar_diary(user_id: str, query: str, top_k: int = 4) -> list[dict]:
    query_vector = get_embedding(query)
    sql_query = text(
        """
        SELECT vector_id, 1 - (diary_vector <=> :query_vector) AS similarity
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
            {"vector_id": row.vector_id, "score": row.similarity} for row in results
        ]
