from pydantic import BaseModel
from typing import List

class CoindcxOrderBookResponse(BaseModel):
    pair : str
    bids: List[List[str]]
    asks: List[List[str]]