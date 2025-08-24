"""
モデルの一元管理

全てのモデルをここからエクスポートして、
Alembicがautogenerate時に認識できるようにする
"""

from .analysis import Analysis
from .auth import GoogleUser, UserGoogleLink
from .base import Base, BaseClass
from .diary import Diary, Message
from .user import User
from .vector import DiaryVector

# Alembic autogenerateのためにすべてのモデルを明示的にエクスポート
__all__ = [
    "Base",
    "BaseClass",
    "User",
    "Analysis",
    "Diary",
    "Message",
    "DiaryVector",
    "GoogleUser",
    "UserGoogleLink",
]
