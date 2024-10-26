ANALYZE_USER_PROMPT = """
これはLINEによるメッセージ送信を使用した日記作成アプリです。
ユーザーがこれまでに送信したすべてのメッセージを分析し、ユーザーの性格、強み、弱みをメッセージを元に生成してください。

- personality: ユーザーの性格
- strength: ユーザーの強み
- weakness: ユーザーの弱み
の3つを生成してください。


Input and Output format:
========================
Input:
- ユーザーの全日記のリスト

Output:
{{
    "personality": "ユーザーの性格",
    "strength": "ユーザーの強み",
    "weakness": "ユーザーの弱み"
}}
========================

Let's get started! 

Input:
{diaries}

Output:
"""
