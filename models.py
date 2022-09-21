import typing as t
from pydantic import BaseModel


class RequestPayload(BaseModel):
    method: str
    url: str
    headers: t.Optional[t.Dict]
    params: t.Optional[t.Dict]
    json_data: t.Optional[t.Dict]
    data: t.Optional[t.Dict]
    timeout: t.Optional[int] = 5
