from datetime import datetime

from app.db.model import Analysis, Diary, Message, User
from app.utils.session_scope import get_session


def add_user(
    session,
    user_id: int,
    name: str,
    mode: str = None,
    icon_url: str = None,
    status_message: str = None,
    link_token: str = None,
) -> User:
    new_user = User(
        user_id=user_id,
        name=name,
        mode=mode,
        icon_url=icon_url,
        status_message=status_message,
        link_token=link_token,
    )
    session.add(new_user)
    session.flush()
    return new_user


def add_analysis(
    session,
    user_id: int,
    personality: str,
    strength: str,
    weakness: str,
) -> Analysis:
    new_analysis = Analysis(
        user_id=user_id,
        personality=personality,
        strength=strength,
        weakness=weakness,
    )
    session.add(new_analysis)
    session.flush()
    return new_analysis


def add_diary(
    session,
    user_id: int,
    date: datetime,
    title: str = None,
    summary: str = None,
    feedback: str = None,
) -> Diary:
    new_diary = Diary(
        user_id=user_id,
        date=date,
        title=title,
        summary=summary,
        feedback=feedback,
    )
    session.add(new_diary)
    session.flush()
    return new_diary


def add_message(
    session,
    diary_id: int,
    user_id: int,
    media_type: str,
    content: str,
) -> Message:
    new_message = Message(
        diary_id=diary_id,
        user_id=user_id,
        media_type=media_type,
        content=content,
    )
    session.add(new_message)
    session.flush()
    return new_message
