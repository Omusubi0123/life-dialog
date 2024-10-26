from enum import Enum


class ModelNames(Enum):
    gpt_4o_mini = "gpt-4o-mini"
    gpt_4o = "gpt-4o"
    gpt_35_turbo = "gpt-3.5-turbo-1106"

    dall_e_3 = "dall-e-3"
    dall_e_2 = "dall-e-2"

    tts_1 = "tts-1"
    tts_1_hd = "tts-1-hd"

    text_embedding_3_large = "text-embedding-3-large"
    text_embedding_3_small = "text-embedding-3-small"
