
import os
from dotenv import load_dotenv
import urllib
from urllib.parse import urlencode, urlparse
import requests

from connectors.kucoin.kucoin_auth import KucoinAuth
from models.kc_response import KucoinOrderBookResponse

load_dotenv()

class Kucoin:
    def __init__(self):
        self.api_key = os.getenv("KC_API_KEY")
        self.auth = KucoinAuth()
        self.base_url = "https://api.kucoin.com"

    def get_order_book(self, _symbol):
        '''
        level2_20 -> gives 20 data
        leve2 -> gives complete data
        '''
        method = "GET"
        endpoint = "/api/v3/market/orderbook/level2_20"
        params = {
            "symbol": _symbol,
        }
        endpoint += ('&', '?')[urlparse(endpoint).query == ''] + urlencode(params)

        auth_data = self.auth.authenticate(method,endpoint)

        full_url = self.base_url + endpoint

        headers = {
            'Content-Type': 'application/json',
            'KC-API-KEY' : self.api_key,
            'KC-API-SIGN' : auth_data["KC-SIGNATURE"],
            'KC-API-TIMESTAMP' : auth_data["KC-TIMESTAMP"],
            'KC-API-PASSPHRASE' : auth_data["KC-PASSPHRASE"],
            'KC-API-KEY-VERSION' : os.getenv('KC_API_KEY_VERSION'),
        }

        response = requests.request(method, full_url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Error fetching order book: {response.status_code} - {response.text}")
        return KucoinOrderBookResponse(**response.json().get('data', {}))

if __name__ == '__main__':
    interactor = Kucoin()
    order_book = interactor.get_order_book(_symbol="BTC-USDT")
    print(order_book)
