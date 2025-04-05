
from pydantic import BaseModel
from typing import List

class BinanceOrderBookResponse(BaseModel):
    lastUpdateId: int
    bids: List[List[str]]
    asks: List[List[str]]