import asyncio
import json
from service.fetcher import OrderBookFetcher
from decimal import Decimal

class OrderBookProcessor:
    def __init__(self):
        self.fetcher = OrderBookFetcher()

    async def fetch_data(self, exchange, symbol):
        return await self.fetcher.get_order_book_data(exchange, symbol)

    def calculate_spread(self, buyer_side, seller_side):
        trade_quantity = min(buyer_side.top_bid_quantity, seller_side.top_ask_quantity)
        if trade_quantity == 0:
            return Decimal('0')

        # buyer_price_per_quantity = buyer_side.top_bid_price / buyer_side.top_bid_quantity
        # seller_price_per_quantity = seller_side.top_ask_price / seller_side.top_ask_quantity
        return (((buyer_side.top_bid_price - seller_side.top_ask_price)) / seller_side.top_ask_price) * 100

    # def calculate_profit(self, buyer_side, seller_side):
    #     trade_quantity = min(buyer_side.top_bid_quantity, seller_side.top_ask_quantity)
    #     if trade_quantity == 0:
    #         return Decimal('0')


    def calculate_opportunity(self, order_books):
        opportunities = []
        for i in range(len(order_books)):
            for j in range(len(order_books)):
                if order_books[i] and order_books[j]:
                    buyer_side = order_books[i]
                    seller_side = order_books[j]
                    if buyer_side.symbol == seller_side.symbol:
                        spread = self.calculate_spread(buyer_side, seller_side)
                        trade_quantity = min(buyer_side.top_bid_quantity, seller_side.top_ask_quantity)
                        if spread > 0.5:
                            opportunities.append({
                                "buyer_side_exchange": buyer_side.exchange,
                                "seller_side_exchange": seller_side.exchange,
                                "buyer_side_price": buyer_side.top_bid_price,
                                "seller_side_price": seller_side.top_ask_price,
                                "buyer_side_quantity": buyer_side.top_bid_quantity,
                                "seller_side_quantity": seller_side.top_ask_quantity,
                                "trade_quantity": trade_quantity,
                                "profit": trade_quantity*(buyer_side.top_bid_price - seller_side.top_ask_price),
                                "spread": spread,
                                "symbol": buyer_side.symbol
                            })
        return opportunities

    async def process(self, exchanges, symbols):
        tasks = []
        for exchange in exchanges:
            for symbol in symbols:
                tasks.append(self.fetch_data(exchange, symbol))
        order_books = await asyncio.gather(*tasks)
        return self.calculate_opportunity(order_books)

async def main():
    processor = OrderBookProcessor()
    exchanges = ["kucoin" , "coinswitch"]
    symbols = ["XRP-USDT", "ETH-USDT", "SOL-USDT", "PEPE-USDT"]
    timer = 0
    while True:
        print(timer, "Seconds ")
        timer += 1
        opportunities = await processor.process(exchanges, symbols)
        if opportunities:
            print(json.dumps(opportunities, indent=4))
            with open("opportunities", "a") as file:
                file.write(json.dumps(opportunities, indent=4) + "\n")
        else:
            print("None")
            with open("opportunities", "a") as file:
                file.write("None\n")
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())