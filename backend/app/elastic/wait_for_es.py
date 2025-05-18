import time
import requests

from app.elasticsearch_settings import es_host

def wait_for_es(timeout: int = 30):
    url = f"{es_host}/_cluster/health"
    for _ in range(timeout):
        try:
            r = requests.get(url)
            if r.status_code == 200 and r.json().get("status") in ("yellow", "green"):
                return
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    raise RuntimeError("Elasticsearch is not ready")
