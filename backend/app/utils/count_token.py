import tiktoken

from app.utils.modelname import ModelNames

encoding = tiktoken.encoding_for_model(ModelNames.gpt_4o.value)


def count_tokens(text: str) -> int:
    return len(encoding.encode(text))
