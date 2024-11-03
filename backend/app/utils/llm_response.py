from openai import OpenAI

from app.settings import settings
from app.utils.modelname import ModelNames

client = OpenAI(api_key=settings.openai_api_key)


def openai_call(
    system_prompt: str,
    user_prompt: str,
    modelname: str = ModelNames.gpt_4o_mini.value,
    json_format: bool = False,
    print_response: bool = False,
) -> str:

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    response = client.chat.completions.create(
        model=modelname,
        messages=messages,
        response_format={"type": "json_object" if json_format else "text"},
        temperature=0.7,
        top_p=0.95,
        timeout=100,
    )

    if print_response:
        print(response.choices[0].message.content)

    return response.choices[0].message.content


def get_embedding(text: str, model: str = ModelNames.text_embedding_3_small.value):
    """embeddingを行う

    Args:
        text (str): embeddingしたい文章
        model (str): embeddingモデル名
    """
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding
