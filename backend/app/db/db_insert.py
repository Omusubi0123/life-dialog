from datetime import datetime

from app.db.model import Analysis, Diary, Message, User
from app.utils.session_scope import session_scope


def add_entity(session, entity):
    with session_scope(session):
        session.add(entity)


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
    add_entity(session, new_user)
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
    add_entity(session, new_analysis)
    return new_analysis


def add_diary(
    session, 
    user_id: int, 
    date: datetime,
    title: str, 
    summary: str, 
    feedback: str,
) -> Diary:
    new_diary = Diary(
        user_id=user_id,
        date=date,
        title=title,
        summary=summary,
        feedback=feedback,
    )
    add_entity(session, new_diary)
    return new_diary


def add_message(
    session,
    message_id: int,
    diary_id: int,
    user_id: int,
    media_type: str,
    content: str,
) -> Message:
    new_message = Message(
        message_id=message_id,
        diary_id=diary_id,
        user_id=user_id,
        media_type=media_type,
        content=content,
    )
    add_entity(session, new_message)
    return new_message
