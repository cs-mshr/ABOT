
import aiohttp
from urllib.parse import urlencode
from models.binance_response import BinanceOrderBookResponse  # Import from separate file

class BinanceExchange:
    def __init__(self):
        self.base_url = 'https://api.binance.com'

    async def get_order_book(self, symbol: str, limit: int = 100) -> BinanceOrderBookResponse:
        endpoint = '/api/v3/depth'
        params = {'symbol': symbol.upper(), 'limit': limit}
        full_url = f"{self.base_url}{endpoint}?{urlencode(params)}"

        async with aiohttp.ClientSession() as session:
            async with session.get(full_url) as response:
                response.raise_for_status()

                data = await response.json()
                return BinanceOrderBookResponse(**data)
