from datetime import datetime, timezone, timedelta
from main import MarketDataFetcher

"""
This is integration test suit for the script to check if its returning the data as expected.
"""
# using time delta to fetch the data from last week to capture future impact of any data change
# this can be used for 1 or 2 days to capture the change more quickly
from_date = datetime.utcnow()-timedelta(7)
# end date till which we need data
to_date = datetime.utcnow()-timedelta(5)
# symbol of the instrument that is supportable by broker
instrument = "BTC-USDT"
# time interval in which we need data , here we are take everyday  close price
interval = "1D"

close_data = MarketDataFetcher("OkxInteractor", conf_path_override="../src/configs").fetch_daily_closing_prices(instrument, interval, from_date, to_date,)

assert close_data != {}
assert len(close_data) == 2


