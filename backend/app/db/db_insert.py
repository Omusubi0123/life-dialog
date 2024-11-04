from datetime import date

from sqlalchemy import update

from app.db.model import Analysis, Diary, DiaryVector, Message, User


def add_user(
    session,
    user_id: str,
    name: str,
    mode: str = None,
    icon_url: str = None,
    status_message: str = None,
    link_token: str = None,
) -> User:
    """ユーザーを追加・既に存在する場合は更新する"""
    stmt = (
        update(User)
        .where(User.user_id == user_id)
        .values(
            name=name,
            mode=mode,
            icon_url=icon_url,
            status_message=status_message,
            link_token=link_token,
        )
    )
    result = session.execute(stmt)

    if result.rowcount == 0:
        # 更新された行がない場合は新規ユーザーを作成
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
    else:
        # 更新が成功した場合は更新されたユーザーを取得して返す
        session.flush()
        return session.query(User).filter(User.user_id == user_id).first()


def add_analysis(
    session,
    user_id: str,
    personality: str,
    strength: str,
    weakness: str,
) -> Analysis:
    stmt = (
        update(Analysis)
        .where(Analysis.user_id == user_id)
        .values(
            personality=personality,
            strength=strength,
            weakness=weakness,
        )
    )
    result = session.execute(stmt)
    if result.rowcount == 0:
        # 更新された行がない場合は新規分析を作成
        new_analysis = Analysis(
            user_id=user_id,
            personality=personality,
            strength=strength,
            weakness=weakness,
        )
        session.add(new_analysis)
        session.flush()
        return new_analysis
    else:
        # 更新が成功した場合は更新された分析を取得して返す
        session.flush()
        return session.query(Analysis).filter(Analysis.user_id == user_id).first()


def add_diary(
    session,
    user_id: str,
    date: date,
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
    user_id: str,
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


def add_diary_vector(
    session,
    user_id: str,
    diary_id: int,
    diary_content: str,
    diary_vector: list[float],
) -> DiaryVector:
    """日記のベクトルを追加・既に存在する場合は更新する"""
    stmt = (
        update(DiaryVector)
        .where(DiaryVector.diary_id == diary_id)
        .values(
            diary_content=diary_content,
            diary_vector=diary_vector,
        )
    )
    result = session.execute(stmt)

    if result.rowcount == 0:
        # 更新された行がない場合は新規ユーザーを作成
        new_diary_vector = DiaryVector(
            user_id=user_id,
            diary_id=diary_id,
            diary_content=diary_content,
            diary_vector=diary_vector,
        )
        session.add(new_diary_vector)
        session.flush()
        return new_diary_vector
    else:
        # 更新が成功した場合は更新されたユーザーを取得して返す
        session.flush()
        return (
            session.query(DiaryVector).filter(DiaryVector.diary_id == diary_id).first()
        )
