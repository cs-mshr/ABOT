from urllib.parse import urlencode, urlparse
from dotenv import load_dotenv
import requests
from connectors.cspro.cspro_auth import CSProAuth

load_dotenv()

class CSPro:
    def _init_(self):
        self.auth = CSProAuth()
        self.base_url = 'https://coinswitch.co'

    def get_exchange_data(self, _symbol):
        method = 'GET'
        _exchange = "coinswitchx"
        params = {
            'exchange': _exchange,
            'symbol': _symbol
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

        response = requests.request("GET",full_url, headers=headers, json=payload)
        return response