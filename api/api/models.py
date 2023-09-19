from pydantic import BaseModel, PastDatetime


class RawData(BaseModel):
    user_id: str
    timestamp: PastDatetime
    lat: float
    long: float
