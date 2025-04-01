import os
from dotenv import load_dotenv
import time
import base64
import hmac
import hashlib


load_dotenv()


def sign(secret_key, message):
    signature = base64.b64encode(hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')
    return signature

class KucoinAuth:
    def __init__(self):
        self.secret_key = os.getenv("KC_SECRET_KEY")
        self.passphrase = os.getenv("KC_PASSPHRASE")

    def authenticate(self, method: str, url, body={}):
        body = body or {}
        now = int(time.time() * 1000)
        string_sign = str(now) + method + url
        signature_signed = sign(self.secret_key, string_sign)
        passphrase_signed = sign(self.secret_key, self.passphrase)

        return {
            'KC-TIMESTAMP': str(now),
            'KC-SIGNATURE': signature_signed,
            'KC-PASSPHRASE': passphrase_signed,
        }










