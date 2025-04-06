import asyncio
import json
from decimal import Decimal

from pydantic import ValidationError

from connectors.cspro.cspro import CSProExchange
from connectors.kucoin.kucoin import Kucoin
from models.common_response import CommonOrderBook

class OrderBookFetcher:
    def __init__(self):
        self.cspro = CSProExchange()
        self.kucoin = Kucoin()
        self.exchange_map = {
            "coinswitch": self.cspro,
            "kucoin": self.kucoin
        }
        self.indian_exchanges = ["coinswitch"] # Add other exchanges which dont support coin/usdt pair
        self.usdt_inr = Decimal(89.5) # took constant value for now , change this for proper conversion;

    def format_symbol(self, exchange, symbol):
        base, quote = symbol.split("-")
        if exchange in self.indian_exchanges and quote == "USDT":
            quote = "INR"

        if exchange == "coinswitch":
            formatted_symbol = f"{base}/{quote}"
        elif exchange == "kucoin":
            formatted_symbol = f"{base}-{quote}"
        else:
            formatted_symbol = symbol

        return formatted_symbol

    async def get_order_book_data(self, exchange, symbol):
        exchange_instance = self.exchange_map.get(exchange)
        if not exchange_instance:
            raise ValueError(f"Exchange {exchange} not supported")

        formatted_symbol = self.format_symbol(exchange, symbol)
        final_orderbook = await exchange_instance.get_order_book(formatted_symbol)

        top_ask_price = Decimal(final_orderbook.asks[0][0])
        top_bid_price = Decimal(final_orderbook.bids[0][0])
        top_bid_quantity = Decimal(final_orderbook.bids[0][1])
        top_ask_quantity = Decimal(final_orderbook.asks[0][1])

        if exchange not in self.indian_exchanges:
            top_bid_price *= self.usdt_inr
            top_ask_price *= self.usdt_inr

        current_exchange_data = {
            "exchange": exchange,
            "top_bid_price": top_bid_price,
            "top_ask_price": top_ask_price,
            "top_bid_quantity": top_bid_quantity,
            "top_ask_quantity": top_ask_quantity,
            "symbol": symbol,
        }

        try:
            validated_result = CommonOrderBook(**current_exchange_data)
            return validated_result
        except ValidationError as e:
            print(f"Validation error: {e}")
            return None

