from app.alg.print_search_result import print_search_result
from app.elastic.sync_diary import es
from app.env_settings import env


def elasticsearch_diary(
    user_id: str, query: str, top_k: int = 4, debug: bool = False
) -> list[dict]:
    print(user_id, query)
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "more_like_this": {
                            "fields": ["diary_content"],
                            "like": query,
                            "min_term_freq": 1,
                            "min_doc_freq": 1,
                        }
                    },
                    {"term": {"user_id.keyword": user_id}},
                ]
            }
        },
        "size": top_k,
    }

    results = es.search(index=env.elasticsearch_index, body=body)

    results = [
        {
            "user_id": hit["_source"]["user_id"],
            "diary_id": hit["_source"]["diary_id"],
            "date": hit["_source"]["date"],
            "diary_content": hit["_source"]["diary_content"],
            "score": hit["_score"],
        }
        for hit in results["hits"]["hits"]
    ]

    if debug:
        print_search_result(results, "bm25", 10)
    return results
