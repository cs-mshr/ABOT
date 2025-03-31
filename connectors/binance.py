# binance_spot.py
import requests
from typing import Optional, Dict, List


class BinanceOrderBook:
    """Binance Spot Order Book with enhanced visualization"""

    def __init__(self, base_url: str = "https://api.binance.com/api/v3"):
        self.base_url = base_url
        self.request_count = 0

    def fetch_order_book(self, symbol: str, limit: int = 10) -> Optional[Dict]:
        """Retrieves full order book with price aggregation"""
        valid_limits = [5, 10, 20, 50, 100, 500, 1000]
        limit = limit if limit in valid_limits else 10

        try:
            response = requests.get(
                f"{self.base_url}/depth",
                params={'symbol': symbol, 'limit': limit}
            )
            response.raise_for_status()
            self.request_count += 1
            return response.json()
        except Exception as e:
            print(f"Error fetching order book: {e}")
            return None

    def visualize_book(self, symbol: str, depth: int = 5, show_qty: bool = True):
        """Displays ASCII order book visualization"""
        book = self.fetch_order_book(symbol, depth * 2)  # Get extra levels for better visualization
        if not book:
            return

        bids = sorted([[float(p), float(q)] for p, q in book['bids']], reverse=True)
        asks = sorted([[float(p), float(q)] for p, q in book['asks']])

        print(f"\n🔍 Order Book: {symbol} (Top {depth} levels)")
        print("-" * 50)
        print(f"{'BIDS (Buyers)':<25} | {'ASKS (Sellers)':>25}")
        print("-" * 50)

        for i in range(depth):
            bid_line = f"{bids[i][0]:<12.8f}"
            ask_line = f"{asks[i][0]:>12.8f}"

            if show_qty:
                bid_line += f" × {bids[i][1]:<8.4f}"
                ask_line = f"{asks[i][1]:>8.4f} × " + ask_line

            print(f"{bid_line:<25} | {ask_line:>25}")

    def get_best_orders(self, symbol: str) -> Optional[Dict]:
        """Returns best bid/ask with liquidity info"""
        book = self.fetch_order_book(symbol, 5)
        if not book:
            return None

        best_bid = [float(book['bids'][0][0]), float(book['bids'][0][1])]
        best_ask = [float(book['asks'][0][0]), float(book['asks'][0][1])]

        return {
            'symbol': symbol,
            'best_bid': best_bid,
            'best_ask': best_ask,
            'spread': best_ask[0] - best_bid[0],
            'spread_pct': (best_ask[0] - best_bid[0]) / best_bid[0] * 100,
            'mid_price': (best_bid[0] + best_ask[0]) / 2
        }