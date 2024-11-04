from linebot import LineBotApi

from app.alg.rag import rag_answer
from app.db.db_insert import add_message
from app.db.get_diary import get_or_create_diary_id
from app.db.manage_user_status import get_user_status, update_user_status
from app.db.set_diary_summary import set_diary_summary
from app.line_bot.quick_reply import create_quick_reply
from app.line_bot.start_loading import start_loading
from app.line_bot.user_status import get_current_status
from app.settings import settings
from app.utils.data_enum import QuickReplyField
from app.utils.get_japan_datetime import get_japan_date
from app.utils.media_enum import MediaType
from app.utils.save_media import save_media
from app.utils.session_scope import get_session

line_bot_api = LineBotApi(settings.channel_access_token)


def handle_text_message(event):
    """テキストメッセージが送信されたときに、現在のユーザーステータスに応じて処理を行う

    Args:
        event (_type_): LINEイベント
    """
    user_id = event.source.user_id
    text = event.message.text

    start_loading(user_id, 60)

    user_status = get_current_status(user_id, event)
    update_user_status(user_id, user_status)

    diary_id = get_or_create_diary_id(user_id, get_japan_date())
    answer, summary, feedback = "", "", ""
    date_list, user_id_list = [], []
    if text not in QuickReplyField.get_values():
        if user_status == QuickReplyField.diary_mode.value:
            # 日記モードの場合はテキストをDBに保存
            with get_session() as session:
                add_message(
                    session,
                    diary_id,
                    user_id,
                    MediaType.TEXT.value,
                    text,
                )
        elif user_status == QuickReplyField.interactive_mode.value:
            # 対話モードの場合はRAGで質問に回答
            answer, date_list, user_id_list = rag_answer(user_id, text)
            # TODO: RAGの質問に対する回答を新しいmedia_typeとしてDBに保存
            # with get_session() as session:
            #     add_message(
            #         session,
            #         diary_id,
            #         user_id,
            #         MediaType.TEXT.value,
            #         f"Q: {text}\nA: {answer}",
            #     )
    elif text == QuickReplyField.view_diary.value:
        _, summary, feedback = set_diary_summary(user_id, diary_id)

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
    diary_id = get_or_create_diary_id(user_id, get_japan_date())
    with get_session() as session:
        add_message(
            session,
            diary_id,
            user_id,
            media_type,
            url,
        )

    # quick replyを作成してline botで返信
    user_status = get_user_status(user_id)
    messages = create_quick_reply(
        event,
        user_status,
        get_japan_date(),
    )
    line_bot_api.reply_message(event.reply_token, messages)
