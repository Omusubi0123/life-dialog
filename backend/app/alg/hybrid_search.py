from app.alg.print_search_result import print_search_result
from app.alg.search_bm25_sim import elasticsearch_diary
from app.alg.search_cosine_sim import cosine_similar_diary


def rrf(
    bm25_ids: list[str], semantic_ids: list[str], top_k: int = 8, rrf_k: int = 60
) -> tuple[list[int], list[float]]:
    """BM25とFAISSの検索結果をRRFでリランキング"""
    bm25_rank_dict = {idx: rank + 1 for rank, idx in enumerate(bm25_ids)}
    semantic_rank_dict = {idx: rank + 1 for rank, idx in enumerate(semantic_ids)}

    all_indices = set(bm25_ids + semantic_ids)
    rrf_scores = {}

    for idx in all_indices:
        bm25_rank = bm25_rank_dict.get(idx, len(bm25_ids) + 1)
        semantic_rank = semantic_rank_dict.get(idx, len(semantic_ids) + 1)
        rrf_score = 1 / (rrf_k + bm25_rank) + 1 / (rrf_k + semantic_rank)
        rrf_scores[idx] = rrf_score

    sorted_indices = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[
        :top_k
    ]

    indices = [idx for idx, _ in sorted_indices]
    scores = [score for _, score in sorted_indices]

    return indices, scores


def hybrid_search(
    user_id: str,
    query: str,
    final_top_k: int = 4,
    temporary_top_k: int = 100,
    debug: bool = False,
) -> list[dict]:
    """ハイブリッド検索を行う関数

    Args:
        user_id (str): ユーザーID
        query (str): 検索クエリ

    Returns:
        list[dict]: 検索結果のリスト
    """
    semantic_results = cosine_similar_diary(
        user_id, query, top_k=temporary_top_k, debug=debug
    )
    semantic_indices = [result["diary_id"] for result in semantic_results]

    bm25_results = elasticsearch_diary(user_id, query, temporary_top_k, debug=debug)
    bm25_indices = [result["diary_id"] for result in bm25_results]

    final_indices, final_scores = rrf(bm25_indices, semantic_indices, top_k=final_top_k)

    final_results = []
    semantic_dict = {result["diary_id"]: result for result in semantic_results}
    bm25_dict = {result["diary_id"]: result for result in bm25_results}

    for idx, score in zip(final_indices, final_scores):
        if idx in semantic_dict:
            result = semantic_dict[idx]
            result["score"] = score
            final_results.append(result)
        elif idx in bm25_dict:
            result = bm25_dict[idx]
            result["score"] = score
            final_results.append(result)

    if debug:
        print_search_result(final_results, "hybrid", top_k=final_top_k)

    return final_results
