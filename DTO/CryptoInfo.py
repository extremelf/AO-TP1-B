from dataclasses import dataclass
from datetime import datetime
from typing import TypedDict

import scrapy
from scrapy import Field


class RecordInfoDTO(scrapy.Item):
    name = Field(serializer=str)
    time_open = Field(serializer=datetime)
    time_close = Field(serializer=datetime)
    time_high = Field(serializer=datetime)
    time_low = Field(serializer=datetime)
    price_open = Field(serializer=float)
    price_high = Field(serializer=float)
    price_low = Field(serializer=float)
    price_close = Field(serializer=float)
    volume = Field(serializer=float)
    marketCap = Field(serializer=float)
    timestamp = Field(serializer=datetime)


@dataclass
class CryptoInfoDTO():
    name: str
    records: list[RecordInfoDTO]
