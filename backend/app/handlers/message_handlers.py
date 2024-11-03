from datetime import date, datetime, timedelta, timezone

from linebot import LineBotApi
from linebot.models import TextSendMessage
from sqlalchemy import update

from app.alg.ai_search_support import upload_diary
from app.alg.analyze_user import analyze_user_by_llm
from app.alg.rag import rag_answer
from app.alg.summarize_diary import summarize_diary_by_llm
from app.db.add_diary_summary import add_diary_summary
from app.db.add_user_analization import add_user_analization
from app.db.db_insert import add_message
from app.db.get_diary_firebase import get_diary_from_db
from app.db.get_diary_id import get_or_create_diary_id
from app.db.manage_user_status import get_user_status, update_user_status
from app.db.model import Diary
from app.db.write_diary import update_doc_field
from app.line_bot.quick_reply import create_quick_reply
from app.line_bot.start_loading import start_loading
from app.line_bot.user_status import get_current_status
from app.settings import settings
from app.utils.data_enum import QuickReplyField
from app.utils.datetime_format import get_YMD_from_datetime
from app.utils.get_japan_datetime import get_japan_date
from app.utils.media_enum import MediaType
from app.utils.media_service import save_media
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
            with get_session() as session:
                message_id = add_message(
                    session,
                    diary_id,
                    user_id,
                    MediaType.TEXT.value,
                    f"Q: {text}\nA: {answer}",
                )
    elif text == QuickReplyField.view_diary.value:
        title, summary, feedback = summarize_diary_by_llm(user_id, get_japan_date())
        with get_session() as session:
            stmt = (
                update(Diary)
                .where(Diary.diary_id == diary_id)
                .values(title=title, summary=summary, feedback=feedback)
            )
            session.execute(stmt)

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

    # message_id = event.message.id

    # # ユーザーのステータスが変更されたらDBに保存
    # # TODO: 下のif分岐の条件式がおかしい　これを入れるとエラーになる
    # # if text in QuickReplyField.get_values() and text != user_status:

    # date = datetime.now(timezone(timedelta(hours=9)))
    # year, month, day = get_YMD_from_datetime(date)
    # answer, summary, feedback = None, None, None
    # date_list, user_id_list = None, None
    # if text not in QuickReplyField.get_values():
    #     timestamp = event.timestamp
    #     if user_status == QuickReplyField.diary_mode.value:
    #         # 日記モードの場合はテキストをDBに保存

    #         print(f"Added message to diary {diary.diary_id}")
    #     elif user_status == QuickReplyField.interactive_mode.value:
    #         # 対話モードの場合はRAGで質問に回答
    #         answer, date_list, user_id_list = rag_answer(user_id, text)
    #         update_doc_field(
    #             user_id,
    #             message_id,
    #             f"Q: {text}\nA: {answer}",
    #             MediaType.TEXT.value,
    #             timestamp,
    #         )
    # elif text == QuickReplyField.view_diary.value:
    #     # TODO: 要約生成、AI searchへアップロードの両方で今日の日記を読み込んでいる
    #     # 日記閲覧の場合は日記の要約・フィードバックを作成しDBに保存
    #     summary, feedback = summarize_diary_by_llm(user_id, year, month, day)
    #     add_diary_summary(user_id, summary, feedback, year, month, day)

    #     # 日記をembeddingしてAI searchのIndexに保存
    #     diary_dict = get_diary_from_db(user_id, year, month, day)
    #     upload_diary(user_id, diary_dict)

    #     # これまでの全日記からユーザーの特徴を分析
    #     personality, strength, weakness = analyze_user_by_llm(event.source.user_id)
    #     add_user_analization(event.source.user_id, personality, strength, weakness)
    # if text == QuickReplyField.interactive_mode.value:
    #     # 日記をembeddingしてAI searchのIndexに保存
    #     diary_dict = get_diary_from_db(user_id, year, month, day)
    #     upload_diary(user_id, diary_dict)

    # # quick replyを作成してline botで返信
    # messages = create_quick_reply(
    #     event,
    #     user_status,
    #     year,
    #     month,
    #     day,
    #     summary,
    #     feedback,
    #     answer,
    #     date_list,
    #     user_id_list,
    # )
    # line_bot_api.reply_message(event.reply_token, messages)


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

    url = save_media(user_id, message_id, message_content, media_type)

    diary_id = get_or_create_diary_id(user_id, date.today())
    with get_session() as session:
        add_message(
            session,
            diary_id,
            user_id,
            media_type,
            url,
        )

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=url))
