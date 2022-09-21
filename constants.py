from pydantic import BaseSettings


class Settings(BaseSettings):
    proxy_redis_host: str = 'localhost'
    proxy_redis_port: int = 6379
    proxy_redis_db: int = 0
    proxy_redis_decode_responses: bool = True
