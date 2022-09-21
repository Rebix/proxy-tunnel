import typing as t
from fastapi import FastAPI
import requests
from redis import Redis

from constants import Settings
from models import RequestPayload

app = FastAPI()

settings = Settings()

proxy_redis = Redis(
    host=settings.proxy_redis_host,
    port=settings.proxy_redis_port,
    db=settings.proxy_redis_db,
    decode_responses=settings.proxy_redis_decode_responses,
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


def get_random_proxy() -> str:
    return proxy_redis.randomkey()


@app.post('/proxy')
def send_req(payload: RequestPayload) -> t.Dict:
    proxy = get_random_proxy()

    if not proxy:
        return {'status': 'Failed', 'message': 'No proxy available.'}

    try:
        res = requests.request(
            payload.method,
            payload.url,
            headers=payload.headers,
            params=payload.params,
            json=payload.json_data,
            data=payload.data,
            timeout=payload.timeout,
            proxies={'http': f'http://{proxy}'},
        )
    except Exception as e:
        return {'status': 'Failed', 'message': 'Request Failed.', 'reason': e}

    try:
        return res.json()
    except Exception as e:
        return {'status': 'Failed', 'message': 'Response decode failed.', 'reason': e}
