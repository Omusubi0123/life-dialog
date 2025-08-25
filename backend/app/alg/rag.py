from datetime import date

from app.alg.hybrid_search import hybrid_search
from app.alg.prompt.rag_prompt import RAG_PROMPT
from app.alg.prompt.system_prompt import SYSTEM_PROMPT
from app.utils.llm_response import openai_call


def format_related_diaries(diaries: list[dict]) -> str:
    def get_date_for_sorting(diary_date):
        """日付を比較可能な形式に変換する"""
        if isinstance(diary_date, date):
            return diary_date
        elif isinstance(diary_date, str):
            # 文字列の場合はdateオブジェクトに変換
            from datetime import datetime
            return datetime.strptime(diary_date, "%Y-%m-%d").date()
        else:
            # その他の場合は文字列として扱う
            return str(diary_date)
    
    # 日付でソート（混在した型を適切に処理）
    diaries.sort(key=lambda x: get_date_for_sorting(x["date"]))
    
    formatted_diaries = "\n".join(
        f"Date: {diary['date']}\nContent: {diary['diary_content']}\n"
        for diary in diaries
    )
    return formatted_diaries


def rag_answer(
    user_id: str,
    query: str,
    system_prompt: str = SYSTEM_PROMPT,
    rag_prompt: str = RAG_PROMPT,
) -> str:
    """対話モードでの質問に対してRAGで回答を生成する

    Args:
        user_id (str): LINEのユーザーID
        query (str): ユーザーの質問

    Returns:
        str: RAGによる回答
    """
    results = hybrid_search(
        user_id, query, final_top_k=10, temporary_top_k=100, debug=False
    )

    date_list = [result["date"] for result in results]
    user_id_list = [result["user_id"] for result in results]
    
    # debug
    for rank, date in enumerate(date_list):
        print(f"rank: {rank}, date: {date}")

    answer = "\n".join(
        [
            f"date: {result['date']}, {result['diary_content'][:100]}"
            for result in results
        ]
    )

    answer = openai_call(
        system_prompt,
        rag_prompt.format(query=query, searched_diary=format_related_diaries(results)),
        print_response=True,
    )

    return answer, date_list, user_id_list
