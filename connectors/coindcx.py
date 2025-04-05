import aiohttp
from pydantic import BaseModel
from models.coindcx_response import CoindcxOrderBookResponse


class CoinDCXExchange:
    def __init__(self):
        self.base_url = 'https://public.coindcx.com'

    async def get_order_book(self, symbol: str) -> CoindcxOrderBookResponse:
        pair = f"B-{symbol.upper()}"
        url = f"{self.base_url}/market_data/orderbook?pair={pair}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                return CoindcxOrderBookResponse(**data)