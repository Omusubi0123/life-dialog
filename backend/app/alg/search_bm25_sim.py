from app.elastic.sync_diary import es
from app.settings import settings

def search_bm25_diary(user_id: str, query: str, top_k: int = 4):
    body = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"diary_content": query}},
                    {"term": {"user_id": user_id}}
                ]
            }
        },
        "size": top_k
    }

    res = es.search(index=settings.elasticsearch_index, body=body)
    return [
        {
            "user_id": hit["_source"]["user_id"],
            "diary_id": hit["_source"]["diary_id"],
            "date": hit["_source"]["date"],
            "diary_content": hit["_source"]["diary_content"],
            "score": hit["_score"],
        }
        for hit in res["hits"]["hits"]
    ]
