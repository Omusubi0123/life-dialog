import json
from datetime import date, datetime
from typing import Any

from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import ResourceNotFoundError
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    HnswVectorSearchAlgorithmConfiguration,
    PrioritizedFields,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SemanticConfiguration,
    SemanticField,
    SemanticSettings,
    SimpleField,
    VectorSearch,
)
from azure.search.documents.models import Vector
from openai import OpenAI

from app.alg.format_diary_for_llm import (
    format_llm_response_json_to_str,
    format_messages_to_llm_input,
)
from app.db.sort_diary_messages import sort_diary_messages_timeorder
from app.settings import settings
from app.utils.data_enum import DiaryField, UserField
from app.utils.modelname import ModelNames

client = OpenAI(api_key=settings.openai_api_key)

search_index_client = SearchIndexClient(
    settings.azure_ai_search_endpoint,
    AzureKeyCredential(settings.azure_ai_search_admin_key),
)

search_client = SearchClient(
    endpoint=settings.azure_ai_search_endpoint,
    index_name=settings.azure_ai_search_index_name,
    credential=AzureKeyCredential(settings.azure_ai_search_admin_key),
)


def create_index(
    search_dimensions: int = 1536,
):
    """AI search Indexを作成"""
    fields = [
        SimpleField(
            name=DiaryField.diary_id.value, type=SearchFieldDataType.String, key=True
        ),
        SearchableField(
            name=UserField.user_id.value,
            type=SearchFieldDataType.String,
            searchable=True,
            retrievable=True,
            filterable=True,
            analyzer_name="ja.microsoft",
        ),
        SearchableField(
            name=DiaryField.date.value,
            type=SearchFieldDataType.String,
            searchable=True,
            retrievable=True,
            analyzer_name="ja.microsoft",
        ),
        SearchableField(
            name="content",
            type=SearchFieldDataType.String,
            searchable=True,
            retrievable=True,
        ),
        SearchField(
            name="contentVector",
            vector_search_dimensions=search_dimensions,
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_configuration="vectorConfig",
        ),
    ]

    vector_search = VectorSearch(
        algorithm_configurations=[
            HnswVectorSearchAlgorithmConfiguration(
                name="vectorConfig",
                kind="hnsw",
            )
        ]
    )

    semantic_config = SemanticConfiguration(
        name="my-semantic-config",
        prioritized_fields=PrioritizedFields(
            title_field=SemanticField(field_name=DiaryField.date.value),
            prioritized_content_fields=[SemanticField(field_name="content")],
            prioritized_keywords_fields=[
                SemanticField(field_name=UserField.user_id.value)
            ],
        ),
    )

    semantic_settings = SemanticSettings(configurations=[semantic_config])

    index = SearchIndex(
        name=settings.azure_ai_search_index_name,
        fields=fields,
        vector_search=vector_search,
        semantic_settings=semantic_settings,
    )

    result = search_index_client.create_index(index)
    print(f" <{result.name} created>")
    return result


def delete_index(index_name: str):
    """Indexを削除

    Args:
        index_name (str): Index名
        settings (Settings): 設定
    """
    result = search_index_client.delete_index(index_name)
    print(f" <{index_name} deleted>")
    return result


def generate_embedding(text: str, model: str = ModelNames.text_embedding_3_small.value):
    """embeddingを行う

    Args:
        text (str): embeddingしたい文章
        model (str): embeddingモデル名
    """
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding


def upload_diary(
    user_id: str,
    doc_dict: dict[str, Any],
    embd_model: str = ModelNames.text_embedding_3_small.value,
):
    """日記をAI search Indexにアップロード

    Args:
        user_id (str): LINEユーザーID
        doc_dict (dict[str, Any]): 日記データ
        embd_model (str, optional): embeddingモデル. Defaults to ModelNames.text_embedding_3_small.value.
    """
    if DiaryField.diary_id.value not in doc_dict:
        print("Error: 'diary_id' not found in doc_dict.")
        return

    sorted_diary_messages = sort_diary_messages_timeorder(doc_dict)

    date_object = datetime.strptime(doc_dict[DiaryField.date.value], "%Y-%m-%d")
    year, month, day = date_object.year, date_object.month, date_object.day

    diary_str = format_messages_to_llm_input(sorted_diary_messages, date.today())
    summary, feedback = doc_dict.get(DiaryField.summary.value), doc_dict.get(
        DiaryField.feedback.value
    )
    recap_str = ""
    if summary and feedback:
        recap_str = format_llm_response_json_to_str(summary, feedback)

    date = f"{year}-{month}-{day}"
    content = recap_str + diary_str
    embedding = generate_embedding(content, model=embd_model)

    document = {
        DiaryField.diary_id.value: doc_dict[DiaryField.diary_id.value],
        UserField.user_id.value: user_id,
        DiaryField.date.value: date,
        "content": content,
        "contentVector": embedding,
    }

    try:
        existing_doc = search_client.get_document(
            key=doc_dict[DiaryField.diary_id.value],
            selected_fields=[DiaryField.diary_id.value],
        )
        search_client.merge_or_upload_documents([document])
        print(f"Document with diary_id {doc_dict[DiaryField.diary_id.value]} updated.")
    except ResourceNotFoundError:
        search_client.upload_documents([document])
        print(
            f"New document with diary_id {doc_dict[DiaryField.diary_id.value]} uploaded."
        )


def hybrid_search(
    user_id: str,
    query: str,
    top: int = 4,
    emdb_model: str = ModelNames.text_embedding_3_small.value,
) -> list[dict[str, Any]]:
    """Azure Hybrid Search

    Args:
        query (str): 検索クエリ
        user_id (str): ユーザーID
        top (int, optional): 結果取得数. Defaults to 10.
        model (str, optional): embeddingモデル名. Defaults to "text-embedding-3-small".

    Returns:
        list[dict[str, Any]]: 検索結果
    """
    query_embedding = generate_embedding(query, model=emdb_model)
    vectors = [
        Vector(
            value=query_embedding,
            k=top,
            fields="contentVector",
        )
    ]

    filter_condition = f"{UserField.user_id.value} eq '{user_id}'"

    results = search_client.search(
        search_text=query,
        vectors=vectors,
        filter=filter_condition,
        top=top,
    )

    results_list = [
        {
            DiaryField.diary_id.value: result[DiaryField.diary_id.value],
            DiaryField.date.value: result[DiaryField.date.value],
            UserField.user_id.value: result[UserField.user_id.value],
            "content": result["content"],
        }
        for result in results
    ]
    return results_list
