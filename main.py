import typing as t
from fastapi import FastAPI
import requests
from redis import Redis

from constants import Settings

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
def send_req(
        method: str, url: str, headers: t.Optional[t.Dict], params: t.Optional[t.Dict],
        json_data: t.Optional[t.Dict], data: t.Optional[t.Dict], timeout: t.Optional[int] = 5,
) -> requests.Response:
    proxy = get_random_proxy()

    res = requests.request(
        method,
        url,
        headers=headers if headers else {},
        params=params if params else {},
        json=json_data if json_data else {},
        data=data if data else {},
        timeout=timeout,
        proxies={'http': f'http://{proxy}'},
    )

    return res
