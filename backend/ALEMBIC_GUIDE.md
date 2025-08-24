# 🚀 Alembic導入ガイド

このプロジェクトでのAlembicマイグレーション管理の完全ガイドです。

## 📁 プロジェクト構造の変更

### 新しい構造（ベストプラクティス）
```
app/
├── models/                    # ✨ NEW: モデル定義（従来のapp/db/model.py）
│   ├── __init__.py           # 全モデルの一元管理
│   ├── base.py              # BaseClass と declarative_base
│   ├── user.py              # User モデル
│   ├── diary.py             # Diary, Message モデル
│   ├── analysis.py          # Analysis モデル
│   └── vector.py            # DiaryVector モデル
├── db/
│   ├── session.py           # ✨ NEW: セッション管理
│   ├── repositories/        # ✨ NEW: リポジトリパターン
│   │   ├── user.py
│   │   ├── diary.py
│   │   └── analysis.py
│   └── config.py           # 従来通り（今後は削除予定）
└── alembic/                # ✨ NEW: マイグレーション管理
    ├── env.py              # 設定済み
    ├── versions/           # マイグレーションファイル
    └── ...
```

## 🔧 Docker環境でのAlembic操作

### 1. 基本操作

#### コンテナ起動
```bash
docker-compose up -d
```

#### マイグレーション生成
```bash
# 自動生成（推奨）
docker-compose exec backend uv run alembic revision --autogenerate -m "マイグレーション名"

# 手動生成
docker-compose exec backend uv run alembic revision -m "マイグレーション名"
```

#### マイグレーション実行
```bash
# 最新まで適用
docker-compose exec backend uv run alembic upgrade head

# 特定のリビジョンまで適用
docker-compose exec backend uv run alembic upgrade <revision_id>

# 1つ前のリビジョンに戻る
docker-compose exec backend uv run alembic downgrade -1
```

#### マイグレーション状況確認
```bash
# 現在の状態
docker-compose exec backend uv run alembic current

# マイグレーション履歴
docker-compose exec backend uv run alembic history

# 未適用のマイグレーション
docker-compose exec backend uv run alembic show head
```

### 2. pgvector対応

初回マイグレーションには既にpgvector拡張の有効化が含まれています：
```python
def upgrade() -> None:
    # Enable pgvector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    # ... その他のマイグレーション
```

新しいVector型カラムを追加する場合：
```python
# マイグレーションファイル内
from pgvector.sqlalchemy import Vector

def upgrade() -> None:
    op.add_column('table_name', sa.Column('vector_column', Vector(1536)))
```

### 3. 開発ワークフロー

#### 3.1 モデル変更からマイグレーションまで

1. **モデル修正**
   ```python
   # app/models/user.py
   class User(BaseClass):
       # 新しいカラムを追加
       new_column = Column(String(100))
   ```

2. **マイグレーション生成**
   ```bash
   docker-compose exec backend uv run alembic revision --autogenerate -m "Add new_column to User"
   ```

3. **生成されたファイルの確認と編集**
   ```python
   # alembic/versions/xxx_add_new_column_to_user.py
   def upgrade() -> None:
       op.add_column('users', sa.Column('new_column', sa.String(length=100)))
   ```

4. **マイグレーション実行**
   ```bash
   docker-compose exec backend uv run alembic upgrade head
   ```

#### 3.2 本番環境への適用

1. **本番前の確認**
   ```bash
   # 未適用マイグレーションの確認
   docker-compose exec backend uv run alembic show head
   
   # SQLを確認（実際には実行しない）
   docker-compose exec backend uv run alembic upgrade head --sql
   ```

2. **本番適用**
   ```bash
   # 本番環境で
   uv run alembic upgrade head
   ```

## 💡 コード変更方針

### 従来のapp/db/使用方法 ❌
```python
# ❌ 古い方法
from app.db.model import User
from app.db.config import SessionLocal

session = SessionLocal()
user = session.query(User).first()
```

### 新しい推奨方法 ✅

#### パターン1: リポジトリパターン（推奨）
```python
# ✅ 新しい方法 - リポジトリパターン
from app.db.session import session_scope
from app.db.repositories import UserRepository

with session_scope() as session:
    user_repo = UserRepository(session)
    user = user_repo.get_by_id("user123")
    # 自動的にcommitされる
```

#### パターン2: FastAPI依存性注入
```python
# ✅ FastAPI での使用
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import User

@app.get("/users/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)):
    return db.query(User).filter(User.user_id == user_id).first()
```

#### パターン3: 直接セッション（注意が必要）
```python
# ⚠️ 手動管理が必要
from app.db.session import get_session
from app.models import User

session = get_session()
try:
    user = session.query(User).first()
    session.commit()
finally:
    session.close()  # 必須！
```

## 🔄 移行手順

### 段階的移行（推奨）

1. **Phase 1**: 新しいモデル構造を並行して導入
   - `app/models/` を作成
   - 既存の `app/db/model.py` はそのまま残す

2. **Phase 2**: 新機能は新構造を使用
   - 新しい機能は `app/models/` を使用
   - リポジトリパターンを採用

3. **Phase 3**: 既存コードを段階的に移行
   - インポート文を変更: `from app.db.model import User` → `from app.models import User`
   - セッション管理を統一

4. **Phase 4**: 旧ファイルを削除
   - `app/db/model.py` を削除
   - `app/db/config.py` を削除

## 🔧 既存DBへのAlembic導入後の対応

### 初期マイグレーションファイルの作成

既存のDBにAlembicを後から導入した場合、**空のDBに対して完全にテーブルを作成するマイグレーションファイル**が必要です。

#### 問題の症状
- 既存のDBでは正常に動作するが、新環境でテーブルが作成されない
- テスト環境や他の開発者の環境でDBセットアップが失敗する

#### 解決済み
現在のプロジェクトでは、以下のマイグレーションファイルが正しく作成されています：
- `10eb8d5b88fb_initial_schema_creation_from_existing_.py`

このファイルには以下が含まれています：
- pgvector拡張の有効化
- 全テーブルの作成（users, analysis, diary, message, diary_vector）
- 適切な外部キー制約
- Vector型の正しい定義

#### 動作確認済み
✅ 空のDBから完全にテーブルを作成可能  
✅ pgvector拡張が正しく有効化される  
✅ 全テーブルとリレーションが正しく作成される  

## ⚠️ 注意事項

### データベース操作時の注意

1. **セッション管理**
   - 必ず適切なセッション管理を行う
   - `session_scope()` の使用を推奨

2. **マイグレーション**
   - 本番適用前に必ずバックアップを取る
   - ステージング環境でテストする

3. **pgvector**
   - Vector型を使用する際はpgvector拡張が有効になっていることを確認
   - ベクトルの次元数を正しく指定する（例: `Vector(1536)`）

## 🎯 ベストプラクティス

1. **マイグレーション名**
   - 分かりやすい名前を付ける
   - 例: `Add user avatar column`, `Create index on diary date`

2. **モデル分割**
   - 関連する機能ごとにファイルを分ける
   - 1ファイル1〜3モデル程度に抑える

3. **リポジトリパターン**
   - データアクセスロジックをリポジトリに集約
   - ビジネスロジックとデータアクセスを分離

4. **型ヒント**
   - すべての関数に適切な型ヒントを付ける
   - Optionalを適切に使用する
