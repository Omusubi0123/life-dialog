from app.alg.prompt.rag_prompt import RAG_PROMPT
from app.alg.prompt.system_prompt import SYSTEM_PROMPT
from app.alg.hybrid_search import hybrid_search
from app.utils.llm_response import openai_call


def format_related_diaries(diaries: list[dict]) -> str:
    diaries.sort(key=lambda x: x["date"])
    formatted_diaries = "\n".join(
        f"Date: {diary['date']}\nContent: {diary['diary_content']}\n" for diary in diaries
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
    results = hybrid_search(user_id, query, final_top_k=10, temporary_top_k=100, debug=False)

    date_list = [result["date"] for result in results]
    user_id_list = [result["user_id"] for result in results]
    
    answer = '\n'.join([f"date: {result['date']}, {result['diary_content'][:100]}" for result in results])

    answer = openai_call(
        system_prompt,
        rag_prompt.format(query=query, searched_diary=format_related_diaries(results)),
        print_response=True,
    )

    return answer, date_list, user_id_list
