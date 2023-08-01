import requests
import time
import base64
import hmac
import hashlib
import json

# Kucoin API credentials
API_KEY = "x"
API_SECRET = "y"
API_PASSPHRASE = "z"

# Get server time
response = requests.get("https://api.kucoin.com/api/v1/timestamp")
server_timestamp = response.json()['data']

# Transfer details
data = {
    "currency": "BTC",
    "from": "main",
    "to": "trade",
    "amount": "0"
}

# Convert the request body to a JSON string
request_body = json.dumps(data)

# Signature
strForSign = f"{server_timestamp}POST/api/v1/accounts/transfer-out{request_body}"
signature = base64.b64encode(hmac.new(bytes(API_SECRET, encoding='utf-8'), bytes(strForSign, encoding='utf-8'), digestmod=hashlib.sha256).digest())

# Passphrase
passphrase = base64.b64encode(hmac.new(bytes(API_SECRET, encoding='utf-8'), bytes(API_PASSPHRASE, encoding='utf-8'), digestmod=hashlib.sha256).digest())

# Headers
headers = {
    "KC-API-KEY": API_KEY,
    "KC-API-SIGN": signature,
    "KC-API-TIMESTAMP": str(server_timestamp),
    "KC-API-PASSPHRASE": passphrase,
    "KC-API-KEY-VERSION": "2",
    "Content-Type": "application/json"
}

# Send request
response = requests.post("https://api.kucoin.com/api/v1/accounts/transfer-out", headers=headers, data=request_body)

# Print the response
print(response.json())