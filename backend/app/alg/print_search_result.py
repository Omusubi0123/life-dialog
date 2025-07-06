from typing import Literal


def print_search_result(
    results: list[dict], search_type: Literal["bm25", "semantic", "hybrid"], top_k: 10
) -> None:
    print("------------------------------------------------")
    print(f"{search_type.capitalize()} Search Results:")
    for rank, result in enumerate(results[:top_k], start=1):
        summary = result["diary_content"][:100].replace("\n", "")
        print(
            f"Rank: {rank}, date: {result['date']}, summary: {summary}, score: {result['score']}"
        )
    print("--------------------------------------------------")
