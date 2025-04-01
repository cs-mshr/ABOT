
from pydantic import BaseModel
from typing import List

class KucoinOrderBookResponse(BaseModel):
    time: int
    sequence : str
    bids: List[List[str]]
    asks: List[List[str]]
