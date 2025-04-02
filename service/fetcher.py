import asyncio
import json
from pydantic import ValidationError

from connectors.cspro.cspro import CSProExchange
from connectors.kucoin.kucoin import Kucoin
from models.common_response import CommonOrderBook

class OrderBookFetcher:
    def __init__(self):
        self.cspro = CSProExchange()
        self.kucoin = Kucoin()
        self.exchange_map = ["coinswitch", "kucoin"]
        self.symbol1 = "btc/inr"
        self.symbol2 = "BTC-USDT"

    async def get_all_orderbooks(self):
        final_orderbooks = await asyncio.gather(
            self.cspro.get_order_book(self.symbol1),
            self.kucoin.get_order_book(self.symbol2)
        )

        results = []
        for i, exchange in enumerate(self.exchange_map):
            current_exchange_data = {
                "exchange": exchange,
                "best_bid": final_orderbooks[i].bids[0],
                "best_ask": final_orderbooks[i].asks[0],
                "symbol": self.symbol2,
            }
            results.append(current_exchange_data)

        validated_results = []
        for result in results:
            try:
                validated_result = CommonOrderBook(**result)
                validated_results.append(validated_result)
            except ValidationError as e:
                print(f"Validation error: {e}")

        return validated_results

    def fetch_and_validate_orderbooks(self):
        return asyncio.run(self.get_all_orderbooks())

