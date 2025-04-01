import os
from cryptography.hazmat.primitives.asymmetric import ed25519
import urllib
from urllib.parse import urlparse, urlencode
from urllib.parse import urlencode, urlparse
from typing import Dict, Any
from dotenv import load_dotenv
import time
import json
import requests

load_dotenv()


def sign(private_key_hex, message):
    private_key_bytes = bytes.fromhex(private_key_hex)
    signing_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)
    signature = signing_key.sign(message.encode('utf-8'))
    return signature.hex()

def gen_sign(secret_key, method, url, body={}):
    body = body or {}
    endpoint_path = url
    timestamp = str(int(time.time() * 1000))

    if method in ["GET", "DELETE"]:
        message = method + endpoint_path + timestamp
    else:
        message = method + endpoint_path + json.dumps(body, separators=(',', ':'), sort_keys=True) + timestamp

    signature = sign(secret_key, message)
    return {
        "Timestamp": timestamp,
        "Signature": signature
    }


class CSXAuth:
    def __init__(self):
        self.api_key = os.getenv("CSX_API_KEY")
        self.secret_key = os.getenv("CSX_SECRET_KEY")

    def rest_authenticate(self, method: str, url: str, payload: Dict[str, Any] = None, params: Dict[str, str] = None) -> \
    Dict[str, str]:
        payload = payload or {}
        url_with_query = url
        if method == "GET" and params:
            url_with_query += ('&', '?')[urlparse(url).query == ''] + urlencode(params)
            url_with_query = urllib.parse.unquote_plus(url_with_query)

        sign_data = gen_sign(self.secret_key, method, url_with_query, payload)

        return {
            "CSX-ACCESS-TIMESTAMP": sign_data["Timestamp"],
            "CSX-SIGNATURE": sign_data["Signature"],
            "CSX-ACCESS-KEY": self.api_key,
            "CSX-EPOCH-TIME": sign_data["Timestamp"],
        }


class CSX:
    def __init__(self):
        self.auth = CSXAuth()
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
