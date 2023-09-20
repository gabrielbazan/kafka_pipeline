from pydantic import BaseModel, PastDatetime


class RawData(BaseModel):  # type: ignore
    user_id: str
    timestamp: PastDatetime
    lat: float
    long: float
