import pandas as pd
from datetime import timezone, datetime, timedelta
from pprint import pprint
from src.errors.api_error import InvalidInputError
import logging
# below import will be used for dynamic object building of broker
from src.interactor.okx_interactor import OkxInteractor

# Set up logging configuration
logging.basicConfig(level=logging.INFO)


class MarketDataFetcher:
    """
    This is main class which will call the fetch daily price for the given instrument and interval
    This class can be extended and compatible enough to support other sources of data.
    """
    def __init__(self, interator_name: str, conf_path_override=None):
        """
        This is to initialize dynamically the source of the data or agent to be used for fetching the data
        Args:
            interator_name: name of broker
            conf_path_override[optional]: it allows user to pass the location for config file to be used

        """
        self.interactor = interator_name
        logging.info(f"broker passed by user: {interator_name}")

        # dynamically importing and creating an object by fetching the config for OKX or any other broker service
        if interator_name in globals():
            # Create an instance of the class
            self.interactor = globals()[interator_name](conf_path_override=conf_path_override)
        elif interator_name in locals():
            self.interactor = locals()[interator_name](conf_path_override=conf_path_override)
        else:
            raise NameError(f"Class '{interator_name}' is not defined")

        logging.info(f"{interator_name} object is created")

    def fetch_daily_closing_prices(self, instruments: str, interval: str, from_date: datetime, to_date: datetime):

        # Fetch the daily close prices for BTC-USD
        logging.info(f"fetching data for {instruments}")
        close_data = self.interactor.get_historical_data(instruments, interval, from_date, to_date)

        return close_data


if __name__ == '__main__':
    """
    This is the entry point of the script.
    below we are setting values to pass for getting the data,
    by modifying parameter value below we will get different data in response.
    
    Note: we can use differ techniques for user input via arg parse or api based etc. 
    """
    logging.info("Starting the script")
    # start date from which we need data
    from_date = datetime(2024, 7, 1).replace(tzinfo=timezone.utc)
    # end date till which we need data
    to_date = datetime(2024, 7, 31).replace(tzinfo=timezone.utc)
    # symbol of the instrument that is supportable by broker
    instrument = "BTC-USDT"
    # time interval in which we need data , here we are take everyday  close price
    interval = "1D"

    close_data = MarketDataFetcher("OkxInteractor").fetch_daily_closing_prices(instrument, interval, from_date, to_date,)
    # we can extend return type to support multiple type of data like df, dict, tuple etc
    # pprint(close_data)
    # Create DataFrame
    df = pd.DataFrame(list(close_data.items()), columns=["datetime", "close_price"])

    # Convert 'datetime' column to datetime type
    df["datetime"] = pd.to_datetime(df["datetime"])

    print(df)

