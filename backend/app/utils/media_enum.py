from enum import Enum


class MediaType(Enum):
    """メディアの種類 Linebotのメディア型でもあるので変更しないこと"""

    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"

    @classmethod
    def get_names(cls) -> list[str]:
        return [dataset_type.name for dataset_type in cls]

    @classmethod
    def get_values(cls) -> list[str]:
        return [dataset_type.value for dataset_type in cls]


class MediaExtension(Enum):
    TEXT = "txt"
    IMAGE = "png"
    VIDEO = "mp4"
    AUDIO = "mp3"
