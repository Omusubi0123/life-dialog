from elasticsearch import Elasticsearch

from app.env_settings import env

es_host = f"{env.elasticsearch_url}:{env.elasticsearch_port}"
es = Elasticsearch(es_host)
