# jphacks Backend

LINE-bot, FastAPI, Firebase, Azure AI Searchを使ったbackend
LINEアプリのチャットから送信したメッセージをDBに保存し、LLMで分析、AI searchで検索しつつRAGする

## 事前準備
1. [LINE Developers](https://developers.line.biz/ja/)にアクセスし、アカウント、プロバイダー、チャネルを作成  
※ここでLINE公式アカウントの作成も行う  
※参考：[LINE Developers公式 - Messaging APIを始めよう](https://developers.line.biz/ja/docs/messaging-api/getting-started/#step-three-confirm-channel)

2. LINE DevelopersのAPIキー情報を取得し、backend/直下に以下の内容の.envを置く  
※`DEPLOYMENT_URL`は、`ngrok`を使って`Webhook URL`を取得した後でそれを書けばよい
```
CHANNEL_ID=
CHANNEL_SECRET=
CHANNEL_ACCESS_TOKEN=

OPENAI_API_KEY=

DEPLOYMENT_URL=
FRONTEND_URL=
```

3. [ngrok](https://ngrok.com/)に登録し、登録後の画面に表示されるCLIインストールコマンドを、OSの種類に応じて実行  
※`ngrok`はgoogleアカウントで登録可能

4. Firestore, Google Cloud Storageの登録
→ API Key取得

5. OpenAI, Azure portalの開発者用アカウント作成  
→ API Key取得

## 実行コマンド
```
poetry install

# FastAPI立ち上げ
poeetry run uvicornapp.main:app --reload

# ngrokを使ってローカルのPORT=8000をWebhookで利用可能なURLに変換
ngrok http 8000
```
`nkrok`コマンド実行後にコンソールに表示される`ngrok`のURLを
- [LINE Official Account Manager](https://manager.line.biz/)内にある作成した公式アカウントのWebhookに`https://negrokのURL/callback`として追加
- `.env`の`DEPLOYMENT_URL`に`https://negrokのURL`と記述  
※WebhookのURLでは、末尾に`/callback`と付けないと、メッセージを送信しても`callback()`関数が呼び出されない

↓

LINEアプリから公式アカウントを登録し、メッセージを送信するとDBに保存され日記の記録が開始される
