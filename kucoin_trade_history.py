import requests
import time
import base64
import hmac
import hashlib
import datetime
import csv

# Kucoin API credentials
API_KEY = "x"
API_SECRET = "y"
API_PASSPHRASE = "z"

# Ticker symbol
symbol = "BTC-USDT"

# Start and end dates (YYYY-MM-DD)
start_date = datetime.datetime.strptime("2023-07-27", "%Y-%m-%d")
end_date = datetime.datetime.strptime("2023-07-31", "%Y-%m-%d")

# Open the CSV file
with open('trade_history.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["Symbol", "Trade ID", "Price", "Volume", "Trade Time", "Side"])

    # Iterate over each day in the date range
    current_date = start_date
    while current_date <= end_date:
        # Convert the current date to a timestamp (in milliseconds)
        start_timestamp = int(time.mktime(current_date.timetuple()) * 1000)
        end_timestamp = start_timestamp + 86400000  # Add 1 day

        # Get server time
        response = requests.get("https://api.kucoin.com/api/v1/timestamp")
        server_timestamp = response.json()['data']

        # Signature
        strForSign = f"{server_timestamp}GET/api/v1/fills?symbol={symbol}&startAt={start_timestamp}&endAt={end_timestamp}"
        signature = base64.b64encode(hmac.new(bytes(API_SECRET, encoding='utf-8'), bytes(strForSign, encoding='utf-8'), digestmod=hashlib.sha256).digest())

        # Passphrase
        passphrase = base64.b64encode(hmac.new(bytes(API_SECRET, encoding='utf-8'), bytes(API_PASSPHRASE, encoding='utf-8'), digestmod=hashlib.sha256).digest())

        # Headers
        headers = {
            "KC-API-KEY": API_KEY,
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(server_timestamp),
            "KC-API-PASSPHRASE": passphrase,
            "KC-API-KEY-VERSION": "2"
        }

        while True:
            # Send request
            response = requests.get(f"https://api.kucoin.com/api/v1/fills?symbol={symbol}&startAt={start_timestamp}&endAt={end_timestamp}", headers=headers)

            # Check if 'data' key is in the response
            if 'data' in response.json():
                # Get the data
                data = response.json()['data']['items']

                # If no data is returned, break the loop
                if not data:
                    break

                # Write the data to the CSV file
                for item in data:
                    writer.writerow([symbol, item['tradeId'], item['price'], item['size'], item['createdAt'], item['side']])

            else:
                # Print the entire response
                print(response.json())
                break

            # Add a delay of 1 second between each request
            time.sleep(1)

        # Move to the next day
        current_date += datetime.timedelta(days=1)