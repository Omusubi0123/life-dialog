from app.alg.ai_search_support import hybrid_search
from app.alg.prompt.rag_prompt import RAG_PROMPT
from app.alg.prompt.system_prompt import SYSTEM_PROMPT
from app.utils.llm_response import openai_call


def rag_answer(
    user_id: str,
    query: str,
    system_prompt: str = SYSTEM_PROMPT,
    rag_prompt: str = RAG_PROMPT,
) -> str:
    search_results = hybrid_search(user_id, query)
    contents_str = "\n\n".join(result["content"] for result in search_results)


    date_list = [result["date"] for result in search_results]


    user_id_list = [result["user_id"] for result in search_results]

    answer = openai_call(
        system_prompt,
        rag_prompt.format(query=query, searched_diary=contents_str),
        print_response=True,
    )

    return answer, date_list, user_id_list
