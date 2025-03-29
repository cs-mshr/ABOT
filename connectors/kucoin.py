class Kucoin:
    def __init__(self, api_key, api_secret, passphrase):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase

    def get_balance(self):
        # Placeholder for actual API call to get balance
        return {"BTC": 0.5, "ETH": 2.0}

    def place_order(self, symbol, side, amount):
        # Placeholder for actual API call to place an order
        return {"order_id": "123456", "status": "success"}