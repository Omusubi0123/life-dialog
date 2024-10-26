from typing import Generator

from openai import OpenAI

from app.settings import settings
from app.utils.modelname import ModelNames


def cotomi_call(
    system_prompt: str,
    user_prompt: str,
    modelname: str = ModelNames.gpt_4o_mini.value,
) -> str:
    client = OpenAI(api_key=settings.openai_api_key)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    response = client.chat.completions.create(
        model=settings.cotomi_model,
        messages=messages,
        temperature=0.7,
        top_p=0.95,
        timeout=100,
    )

    return response.choices[0].message.content
