
from pydantic import BaseModel
from typing import List

class CommonOrderBook(BaseModel):
    exchange: str
    symbol: str
    best_bid: List[str]
    best_ask: List[str]
