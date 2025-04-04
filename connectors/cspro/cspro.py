from urllib.parse import urlencode, urlparse

import aiohttp
from dotenv import load_dotenv
import requests
from connectors.cspro.cspro_auth import CSProAuth
from models.cspro_response import CSProOrderBookResponse
from utils import logger

load_dotenv()

_logger = logger.get_logger(__name__)

class CSProExchange:
    def __init__(self):
        self.auth = CSProAuth()
        self.base_url = 'https://coinswitch.co'

    async def get_order_book(self, symbol: str):
        method = 'GET'
        exchange = "coinswitchx"
        params = {
            'exchange': exchange,
            'symbol': symbol
        }
        endpoint = '/trade/api/v2/depth'

        payload = {}
        auth_data = self.auth.rest_authenticate(method, endpoint, payload, params)

        endpoint += ('&', '?')[urlparse(endpoint).query == ''] + urlencode(params)
        full_url  = self.base_url + endpoint

        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-SIGNATURE': auth_data["CSX-SIGNATURE"],
            'X-AUTH-APIKEY': auth_data["CSX-ACCESS-KEY"],
            'X-AUTH-EPOCH': auth_data["CSX-EPOCH-TIME"],
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(full_url, headers=headers, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Error fetching order book: {response.status} - {response.text}")
                data = await response.json()
                return CSProOrderBookResponse(**data.get('data', {}))


