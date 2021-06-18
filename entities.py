from datetime import datetime

from pydantic import BaseModel


class Currency(BaseModel):
    ticker: str
    open_time: datetime
    open: float
    close: float
    high: float
    low: float
    volume: float
    time_frame: str
