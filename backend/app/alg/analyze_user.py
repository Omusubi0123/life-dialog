import json

from app.alg.format_diary_for_llm import (
    format_llm_response_json_to_str,
    format_messages_to_llm_input,
)
from app.alg.prompt.analyze_user_prompt import ANALYZE_USER_PROMPT
from app.alg.prompt.system_prompt import SYSTEM_PROMPT_JSON
from app.db.get_diary import get_user_all_diary
from app.db.get_message import get_date_message
from app.utils.count_token import count_tokens
from app.utils.llm_response import openai_call
from app.utils.modelname import ModelNames


def analyze_user_by_llm(
    user_id: str,
    system_prompt: str = SYSTEM_PROMPT_JSON,
    summarize_diary_prompt: str = ANALYZE_USER_PROMPT,
    print_response: bool = True,
) -> tuple[str, str, str]:
    """ユーザーの全日記からユーザーの性格・強み・弱みをLLMで生成する

    Returns:
        LLMによるユーザーの性格・強み・弱み
    """
    diary_list = get_user_all_diary(user_id)
    messages_list = [get_date_message(user_id, diary["date"]) for diary in diary_list]
    print(f"Total diaries: {len(diary_list)}")

    diaries_str = ""
    # LLMのcontext lengthまで日記を追加。最新の日記から入れるために逆順で処理
    for message, diary in reversed(list(zip(messages_list, diary_list))):
        diary_str = format_llm_response_json_to_str(
            diary.get("title"), diary.get("summary")
        )
        diariy_str += format_messages_to_llm_input(message, diary["date"])
        diary_str += "\n\n"

        if len(diaries_str + diariy_str) > 120000:
            break
        diaries_str = diary_str + diaries_str
        print(f"Current diary length: {count_tokens(diaries_str)} tokens")

    result = openai_call(
        system_prompt,
        summarize_diary_prompt.format(diaries=diaries_str),
        print_response=print_response,
        model_name=ModelNames.gpt_4o,
        json_format=True,
    )

    result_dict = json.loads(result)

    personality = result_dict.get("personality", "")
    strength = result_dict.get("strength", "")
    weakness = result_dict.get("weakness", "")
    return personality, strength, weakness


if __name__ == "__main__":
    user_id = "test_user"
    personality, strength, weakness = analyze_user_by_llm(user_id)
    print(f"Personality: {personality}")
    print(f"Strength: {strength}")
    print(f"Weakness: {weakness}")
