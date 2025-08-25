"""
DBにある全てのDiaryを調べて、DiaryVectorが存在しない日があったら、
set_diary_vector()を実行するマイグレーションスクリプト
"""

from datetime import date
from typing import List, Tuple

from sqlalchemy.orm import Session

from app.db.model import Diary, DiaryVector
from app.db.session import session_scope
from app.db.set_diary_vector import set_diary_vector
from app.utils.get_japan_datetime import get_japan_time


def get_diaries_without_vectors(session: Session) -> List[Tuple[str, date]]:
    """DiaryVectorが存在しないDiaryのuser_idと日付のリストを取得する
    
    Args:
        session: SQLAlchemyセッション
        
    Returns:
        List[Tuple[str, date]]: (user_id, date)のタプルのリスト
    """
    # LEFT JOINでDiaryVectorが存在しないDiaryを取得
    query = (
        session.query(Diary.user_id, Diary.date)
        .outerjoin(DiaryVector, Diary.diary_id == DiaryVector.diary_id)
        .filter(DiaryVector.diary_id.is_(None))
        .order_by(Diary.user_id, Diary.date)
    )
    
    return query.all()


def migrate_diary_vectors() -> None:
    """DiaryVectorが存在しないDiaryに対してset_diary_vectorを実行する"""
    
    print(f"開始時刻: {get_japan_time()}")
    print("DiaryVectorが存在しないDiaryを検索中...")
    
    with session_scope() as session:
        missing_vectors = get_diaries_without_vectors(session)
    
    if not missing_vectors:
        print("DiaryVectorが存在しないDiaryは見つかりませんでした。")
        return
    
    print(f"DiaryVectorが存在しないDiary数: {len(missing_vectors)}")
    print("ベクトル生成を開始します...")
    
    success_count = 0
    error_count = 0
    
    for user_id, diary_date in missing_vectors:
        try:
            print(f"処理中: ユーザーID={user_id}, 日付={diary_date}")
            result = set_diary_vector(user_id, diary_date)
            
            if result:
                success_count += 1
                print(f"✓ 成功: ユーザーID={user_id}, 日付={diary_date}")
            else:
                error_count += 1
                print(f"✗ 失敗: ユーザーID={user_id}, 日付={diary_date}")
                
        except Exception as e:
            error_count += 1
            print(f"✗ エラー: ユーザーID={user_id}, 日付={diary_date}, エラー内容: {str(e)}")
    
    print("\n" + "="*50)
    print("マイグレーション完了")
    print(f"処理対象数: {len(missing_vectors)}")
    print(f"成功数: {success_count}")
    print(f"失敗数: {error_count}")
    print(f"完了時刻: {get_japan_time()}")
    print("="*50)


def check_missing_diary_vectors() -> None:
    """DiaryVectorが存在しないDiaryの数をチェックする（実行前確認用）"""
    
    print(f"チェック開始時刻: {get_japan_time()}")
    print("DiaryVectorが存在しないDiaryを検索中...")
    
    with session_scope() as session:
        missing_vectors = get_diaries_without_vectors(session)
    
    if not missing_vectors:
        print("DiaryVectorが存在しないDiaryは見つかりませんでした。")
        return
    
    print(f"\nDiaryVectorが存在しないDiary数: {len(missing_vectors)}")
    print("\n対象のDiary一覧:")
    print("-" * 40)
    
    for user_id, diary_date in missing_vectors:
        print(f"ユーザーID: {user_id}, 日付: {diary_date}")
    
    print("-" * 40)
    print(f"チェック完了時刻: {get_japan_time()}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        # チェックモード：実行せずに対象数を確認
        check_missing_diary_vectors()
    else:
        # 実行モード：実際にベクトル生成を実行
        print("DiaryVectorマイグレーションを開始します...")
        print("事前チェックを実行しますか？ (y/n): ", end="")
        
        # 実際のプロダクション環境では入力を求めずに実行する場合は下記をコメントアウト
        # choice = input().lower()
        # if choice == 'y':
        #     check_missing_diary_vectors()
        #     print("\n実際のマイグレーションを実行しますか？ (y/n): ", end="")
        #     choice = input().lower()
        #     if choice != 'y':
        #         print("マイグレーションをキャンセルしました。")
        #         sys.exit(0)
        
        migrate_diary_vectors()
