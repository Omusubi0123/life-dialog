RAG_PROMPT = """
ユーザーが検索した自分の日記をもとに、質問に回答してください。

Input:
- {query}: ユーザーが検索した質問
- {searched_diary}: ユーザーが検索した日記

Output:
"""
