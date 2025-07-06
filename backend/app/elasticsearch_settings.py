from elasticsearch import Elasticsearch

from app.settings import settings

es_host = f"{settings.elasticsearch_url}:{settings.elasticsearch_port}"
es = Elasticsearch(es_host)
