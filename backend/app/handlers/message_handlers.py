from linebot import LineBotApi

from app.alg.rag import rag_answer
from app.db.repositories.diary import DiaryRepository, MessageRepository
from app.db.repositories.user import UserRepository
from app.db.set_diary_summary import set_diary_summary
from app.env_settings import env
from app.line_bot.quick_reply import create_quick_reply
from app.line_bot.start_loading import start_loading
from app.line_bot.user_status import get_current_status
from app.utils.data_enum import QuickReplyField
from app.utils.get_japan_datetime import get_japan_date
from app.utils.media_enum import MediaType
from app.utils.save_media import save_media
from app.utils.session_scope import get_session

line_bot_api = LineBotApi(env.channel_access_token)


def handle_text_message(event):
    """テキストメッセージが送信されたときに、現在のユーザーステータスに応じて処理を行う

    Args:
        event (_type_): LINEイベント
    """
    user_id = event.source.user_id
    text = event.message.text

    start_loading(user_id, 60)

    user_status = get_current_status(user_id, event)

    with get_session() as session:
        user_repo = UserRepository(session)
        diary_repo = DiaryRepository(session)
        message_repo = MessageRepository(session)

        user_repo.update_status(user_id, user_status)

        diary = diary_repo.get_or_create_by_user_and_date(user_id, get_japan_date())
        diary_id = diary.diary_id

        answer, summary, feedback = "", "", ""
        date_list, user_id_list = [], []
        if text not in QuickReplyField.get_values():
            if user_status == QuickReplyField.diary_mode.value:
                # 日記モードの場合はテキストをDBに保存
                message_repo.create(
                    diary_id,
                    user_id,
                    MediaType.TEXT.value,
                    text,
                )
                session.commit()
            elif user_status == QuickReplyField.interactive_mode.value:
                # 対話モードの場合はRAGで質問に回答
                answer, date_list, user_id_list = rag_answer(user_id, text)
                # TODO: RAGの質問に対する回答を新しいmedia_typeとしてDBに保存
                # message_repo.create(
                #     diary_id,
                #     user_id,
                #     MediaType.TEXT.value,
                #     f"Q: {text}\nA: {answer}",
                # )
        elif text == QuickReplyField.view_diary.value:
            _, summary, feedback = set_diary_summary(user_id, diary_id)

        session.commit()

    # quick replyを作成してline botで返信
    messages = create_quick_reply(
        event,
        user_status,
        get_japan_date(),
        summary,
        feedback,
        answer,
        date_list,
        user_id_list,
    )
    line_bot_api.reply_message(event.reply_token, messages)


def handle_media_message(event):
    """画像ファイルが送信されたときに、DBに保存しURLを返す

    Args:
        event (_type_): LINEイベント
    """
    user_id = event.source.user_id
    media_type = event.message.type

    start_loading(user_id, 60)

    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)

    # メディアをnginxに保存
    url = save_media(user_id, message_id, message_content, media_type)

    # メディアのURLをMessage DBに保存
    with get_session() as session:
        diary_repo = DiaryRepository(session)
        message_repo = MessageRepository(session)
        user_repo = UserRepository(session)

        diary = diary_repo.get_or_create_by_user_and_date(user_id, get_japan_date())
        diary_id = diary.diary_id

        message_repo.create(
            diary_id,
            user_id,
            media_type,
            url,
        )

        session.commit()

        # quick replyを作成してline botで返信
        user = user_repo.get_by_id(user_id)
        user_status = user.mode if user else None
    messages = create_quick_reply(
        event,
        user_status,
        get_japan_date(),
    )
    line_bot_api.reply_message(event.reply_token, messages)
