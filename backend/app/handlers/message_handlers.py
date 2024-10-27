from datetime import datetime

from linebot import LineBotApi

from app.alg.ai_search_support import upload_diary
from app.alg.analyze_user import analyze_user_by_llm
from app.alg.rag import rag_answer
from app.alg.summarize_diary import summarize_diary_by_llm
from app.db.add_diary_summary import add_diary_summary
from app.db.add_user_analization import add_user_analization
from app.db.get_diary import get_diary_from_db
from app.db.manage_user_status import get_user_status, update_user_status
from app.db.write_diary import update_doc_field
from app.line_bot.quick_reply import create_quick_reply
from app.line_bot.user_status import get_current_status
from app.settings import Settings
from app.utils.data_enum import QuickReplyField
from app.utils.datetime_format import get_YMD_from_datetime
from app.utils.media_enum import MediaType

settings = Settings()
line_bot_api = LineBotApi(settings.channel_access_token)


def handle_text_message(event):
    """テキストメッセージをDBに保存しオウム返し"""
    user_id = event.source.user_id
    message_id = event.message.id
    text = event.message.text

    user_status = get_current_status(event)

    # ユーザーのステータスが変更されたらDBに保存
    # TODO: 下のif分岐の条件式がおかしい　これを入れるとエラーになる
    # if text in QuickReplyField.get_values() and text != user_status:
    update_user_status(user_id, user_status)

    date = datetime.now()
    year, month, day = get_YMD_from_datetime(date)
    answer, summary, feedback = None, None, None
    date_list, user_id_list = None, None
    if text not in QuickReplyField.get_values():
        timestamp = event.timestamp

        if user_status == QuickReplyField.diary_mode.value:
            # 日記モードの場合はテキストをDBに保存
            update_doc_field(user_id, message_id, text, MediaType.TEXT.value, timestamp)
        elif user_status == QuickReplyField.interactive_mode.value:
            # 対話モードの場合はRAGで質問に回答
            answer, date_list, user_id_list = rag_answer(user_id, text)
            update_doc_field(
                user_id,
                message_id,
                f"Q: {text}\nA: {answer}",
                MediaType.TEXT.value,
                timestamp,
            )
    elif text == QuickReplyField.view_diary.value:
        # TODO: 要約生成、AI searchへアップロードの両方で今日の日記を読み込んでいる
        # 日記閲覧の場合は日記の要約・フィードバックを作成しDBに保存
        summary, feedback = summarize_diary_by_llm(user_id, year, month, day)
        add_diary_summary(user_id, summary, feedback, year, month, day)

        # 日記をembeddingしてAI searchのIndexに保存
        diary_dict = get_diary_from_db(user_id, year, month, day)
        upload_diary(user_id, diary_dict)

        # これまでの全日記からユーザーの特徴を分析
        personality, strength, weakness = analyze_user_by_llm(event.source.user_id)
        add_user_analization(event.source.user_id, personality, strength, weakness)
    if text == QuickReplyField.interactive_mode.value:
        # 日記をembeddingしてAI searchのIndexに保存
        diary_dict = get_diary_from_db(user_id, year, month, day)
        upload_diary(user_id, diary_dict)

    # quick replyを作成してline botで返信
    messages = create_quick_reply(
        event,
        user_status,
        year,
        month,
        day,
        summary,
        feedback,
        answer,
        date_list,
        user_id_list,
    )
    line_bot_api.reply_message(event.reply_token, messages)


def handle_media_message(event):
    """画像ファイルをDBに保存しURLを返す"""
    user_id = event.source.user_id
    message_id = event.message.id
    media_type = event.message.type
    timestamp = event.timestamp
    message_content = line_bot_api.get_message_content(message_id)
    update_doc_field(user_id, message_id, message_content, media_type, timestamp)

    date = datetime.now()
    year, month, day = get_YMD_from_datetime(date)
    user_status = get_user_status(user_id)
    messages = create_quick_reply(
        event,
        user_status,
        year,
        month,
        day,
    )
    line_bot_api.reply_message(event.reply_token, messages)
