import requests
from datetime import timezone, datetime, timedelta
url ="https://www.okx.com/api/v5/market/candles"


data = dict()
# Set up parameters for the API request
from_date = datetime(2024, 10, 1).replace(tzinfo=timezone.utc)
    # end date till which we need data
to_date = datetime(2024, 10, 1).replace(tzinfo=timezone.utc)  + timedelta(days=7)
params = {
    "instId": "BTC-USDT",
    "bar": "1D",
    "before": int(from_date.timestamp() * 1e3),
    "after": int(to_date.timestamp() * 1e3)
}


# Send the request
response = requests.get(url, params=params)
# Check for a successful response
if response.status_code != 200:
    data['msg'] = "Error fetching data"
    data["statusCode"] = response.status_code

print(response.json())

response_data = response.json()

# Process and store the close prices
for candle in response_data['data']:
    close_time = datetime.fromtimestamp(int(candle[0]) / 1000)
    close_price = float(candle[4])
    data[close_time] = [close_price]

print(data)