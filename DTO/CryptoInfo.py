from datetime import datetime
from typing import TypedDict


class RecordInfoDTO(TypedDict):
    time_open: datetime
    time_close: datetime
    time_high: datetime
    time_low: datetime
    price_open: float
    price_high: float
    price_low: float
    price_close: float
    volume: float
    marketCap: float
    timestamp: datetime


class CryptoInfoDTO(TypedDict):
    name: str
    records: list[RecordInfoDTO]




