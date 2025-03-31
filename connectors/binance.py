import requests
from typing import List, Tuple, Optional


class BinanceOrderBook:
    """Binance Spot Order Book with top 5 bids/asks storage"""

    def __init__(self, symbol: str = "BTCUSDT"):
        """
        Initialize order book with top 5 bids and asks
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
        """
        self.base_url = "https://api.binance.com/api/v3"
        self.symbol = symbol
        self.top_bids: List[Tuple[float, float]] = []
        self.top_asks: List[Tuple[float, float]] = []
        self.timestamp: Optional[int] = None
        self._fetch_order_book()

    def _fetch_order_book(self) -> None:
        """Fetch and store top 5 bids and asks"""
        try:
            response = requests.get(
                f"{self.base_url}/depth",
                params={'symbol': self.symbol, 'limit': 5},  # Get exactly 5 levels
                timeout=5
            )
            response.raise_for_status()
            data = response.json()

            # Store top 5 bids (sorted highest to lowest)
            self.top_bids = sorted(
                [(float(p), float(q)) for p, q in data['bids']],
                key=lambda x: -x[0]  # Sort by price descending
            )[:5]

            # Store top 5 asks (sorted lowest to highest)
            self.top_asks = sorted(
                [(float(p), float(q)) for p, q in data['asks']],
                key=lambda x: x[0]  # Sort by price ascending
            )[:5]

            self.timestamp = data['lastUpdateId']

        except Exception as e:
            print(f"Error fetching order book: {e}")

    def refresh(self) -> None:
        """Refresh the order book data"""
        self._fetch_order_book()

    @property
    def best_bid(self) -> Optional[Tuple[float, float]]:
        """Get single best bid (price, quantity)"""
        return self.top_bids[0] if self.top_bids else None

    @property
    def best_ask(self) -> Optional[Tuple[float, float]]:
        """Get single best ask (price, quantity)"""
        return self.top_asks[0] if self.top_asks else None

    @property
    def all_bids(self) -> List[Tuple[float, float]]:
        """Get all 5 bids (price, quantity)"""
        return self.top_bids

    @property
    def all_asks(self) -> List[Tuple[float, float]]:
        """Get all 5 asks (price, quantity)"""
        return self.top_asks

    @property
    def spread(self) -> Optional[float]:
        """Calculate spread between best bid and ask"""
        if self.top_bids and self.top_asks:
            return self.top_asks[0][0] - self.top_bids[0][0]
        return None

