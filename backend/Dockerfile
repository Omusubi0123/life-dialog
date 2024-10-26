# ベースイメージとしてPythonのスリム版を使用
FROM --platform=linux/amd64 python:3.10-slim

# 作業ディレクトリを/appに設定
WORKDIR /app

# 環境変数を設定
ENV PORT=8080

# Poetry のインストール
RUN pip install --no-cache-dir poetry

# pyproject.toml と poetry.lock ファイルをコピー
COPY pyproject.toml poetry.lock ./

# 依存関係をインストール（仮想環境を無効化してインストール）
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

# gunicornをインストール
RUN pip install gunicorn

# アプリケーションコードをコピー
COPY . .

# Dockerfileをコピー
# COPY .env ./

# firebaseの認証情報をコピー
COPY firebase_credential.json /app/firebase_credential.json
ENV GOOGLE_APPLICATION_CREDENTIALS="firebase_credential.json"

# コンテナが使用するポートを指定
EXPOSE 8080

# gunicornとuvicornでアプリケーションを起動
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "-b", "0.0.0.0:8080"]