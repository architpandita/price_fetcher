from abc import ABC
from datetime import datetime
from src.configs.fetch_config import YamlParser
from src.errors.api_error import InvalidResponseError
from src.interactor.base_interactor import BaseInteractor
from src.models.schema import PriceData
import requests, logging

# Set up logging configuration
from src.validations.response_validation import run_get_historical_response_validation

logging.basicConfig(level=logging.INFO)


class OkxInteractor(BaseInteractor, ABC):

    def __init__(self, conf_path_override=None, **kwargs):
        super().__init__(**kwargs)
        logging.info(f"initializing OkxInteractor")
        # getting the configuration for given interactor
        self.config = YamlParser().read_config("interactor_config.yaml", conf_path_override)["okx"]
        logging.info(f"configuration found: {self.config}")
        self.host_url = self.config.get("host_url")

    def get_historical_data(self, instrument: str, interval: str, from_date: datetime, to_date: datetime, price_type: str ="close") -> dict:
        """
        This function will call the broker api with below params to get historical data.
        Args:
            instrument: symbol of the product data is needed
            interval: time frame of the data
            from_date: start date of the data
            to_date: end date till data is needed

        Returns:
                data in dictionary type with time and respective closed price
        """
        url = self.config["host_url"]+"/market/candles"
        logging.info(f"full endpoint formed is {url}")
        ohlc_map = {
                "datetime": 0,
                "open":1,
                "high":2,
                "low": 3,
                "close":4
                }
        data = dict()
        # Set up parameters for the API request
        params = {
            "instId": instrument,
            "bar": interval,
            "before": int(from_date.timestamp() * 1e3),
            "after": int(to_date.timestamp() * 1e3)
        }
        logging.info(f"using params: {params}")

        # Send the request
        response = requests.get(url, params=params)
        # Check for a successful response
        if response.status_code != 200:
            data['msg'] = "Error fetching data"
            data["statusCode"] = response.status_code

            logging.info(f"Error fetching data: {data['msg']}, status code: {data['statusCode']}")
            return data

        response_data = response.json()
        # validate response data

        if PriceData(**response_data):
            logging.info("response data is valid")
        else:
            logging.info("response data is invalid")
            raise InvalidResponseError("invalid response received")

        logging.info(f"data received")
        num_of_days = (to_date - from_date).days
        # running validations on response data for close price
        run_get_historical_response_validation(response_data['data'], **{"num_of_days":num_of_days})

        # Process and store the close prices
        for candle in response_data['data']:
            close_time = datetime.fromtimestamp(int(candle[ohlc_map["datetime"]]) / 1000).strftime("%m-%d-%Y %H:%M:%S")
            close_price = float(candle[ohlc_map[price_type]])
            data[close_time] = close_price
        logging.info(f"data is processed.")

        return data

    def get_multiple_historical_data(self, instruments: list, interval: str, from_date: datetime, to_date: datetime) -> dict:
        """
        This function will call the broker api with below params to get historical data.
        Note: this will take first argument as list, so multiple symbol data can be fetch at same time.
        Args:
            instruments: list of symbol of the product data is needed
            interval: time frame of the data
            from_date: start date of the data
            to_date: end date till data is needed

        Returns:
                data in dictionary type with time and respective closed price for each given instrument

        """
        data = dict()
        logging.info(f"fetching the data for {instruments}")

        for inst in instruments:
            if inst:
                try:
                    data[inst] = self.get_historical_data(inst, interval, from_date, to_date)
                except Exception as e:
                    logging.info(e.__str__())
                    data[inst] = []

        logging.info(f"data is processed.")
        return data
