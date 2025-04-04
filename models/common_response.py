from pydantic import BaseModel
from typing import List

class CommonOrderBook(BaseModel):
    exchange: str
    symbol: str
    top_bid_price: float
    top_ask_price: float
    top_bid_quantity: float
    top_ask_quantity: float