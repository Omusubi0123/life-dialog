from app.alg.prompt.rag_prompt import RAG_PROMPT
from app.alg.prompt.system_prompt import SYSTEM_PROMPT
from app.alg.search_cosine_sim import cosine_similar_diary
from app.utils.llm_response import openai_call


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
    results = cosine_similar_diary(user_id, query)

    contents_str = "\n\n".join(result["diary_content"] for result in results)
    date_list = [result["date"] for result in results]
    user_id_list = [result["user_id"] for result in results]

    answer = openai_call(
        system_prompt,
        rag_prompt.format(query=query, searched_diary=contents_str),
        print_response=True,
    )

    return answer, date_list, user_id_list
