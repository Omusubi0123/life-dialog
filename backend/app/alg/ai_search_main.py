import json
from typing import Any

from openai import OpenAI

from app.alg.ai_search_support import (
    create_index,
    delete_index,
    hybrid_search,
    upload_diary,
)
from app.db.get_diary import get_diary_from_db


def upload_diary_to_ai_search(
    user_id: str,
    diary_dict: dict[str, Any],
    create: bool = False,
    delete: bool = False,
    upload: bool = False,
):
    """AI Searchのメイン処理

    Args:
        index_name (str): Index名
        create (bool, optional): Indexを作成するか. Defaults to False.
        upload (bool, optional): Indexにドキュメントを追加するか. Defaults to False.
        search (bool, optional): AI searchの検索を行うか. Defaults to True.
        load_path (str, optional): ドキュメントのjsonファイルパス. Defaults to os.path.join("ai_search", "data", "filesearch", "filesearch_data.json").
        save_path (str, optional): ベクトル埋め込み付きドキュメントデータのファイルパス. Defaults to os.path.join("ai_search", "data", "filesearch", "filesearch_vector.json").
    """
    if create:
        create_index()
    if delete:
        delete_index()
    if upload:
        upload_diary(user_id, diary_dict)


def search(user_id: str, query: str) -> list[dict[str, Any]]:
    """AI Searchの検索処理"""
    while True:
        query = input("Q: ")
        results = hybrid_search(
            user_id,
            query,
        )
        result_str = json.dumps(results, ensure_ascii=False, indent=4)
        print(result_str)


if __name__ == "__main__":
    data = {
        "user_id": "U304753f9739f31a9191e7b4e1543e9e1",
        "query": "10月26日には何があった?",
        "year": 2024,
        "month": 10,
        "day": 26,
    }

    diary_dict = get_diary_from_db(
        data["user_id"], data["year"], data["month"], data["day"]
    )
    upload_diary_to_ai_search(data["user_id"], diary_dict, create=True, upload=True)

    search(data["user_id"], data["query"])
