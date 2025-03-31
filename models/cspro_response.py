
from pydantic import BaseModel
from typing import List

class CSProOrderBookResponse(BaseModel):
    symbol: str
    timestamp: int
    bids: List[List[str]]
    asks: List[List[str]]
