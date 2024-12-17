import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.interactor.okx_interactor import OkxInteractor


# Sample input data for testing
instrument = "BTC-USDT"
interval = "1D"
from_date = datetime(2024, 10, 1)
to_date = datetime(2024, 10, 2)
sample_candle_data = [
    ["1727740800000", "16800.0", "16900.0", "16750.0", "16850.0", "1000"],
    ["1727827200000", "16850.0", "17000.0", "16800.0", "16950.0", "800"],
]


@pytest.fixture
def interactor():
    return OkxInteractor(conf_path_override="./src/configs")


@patch("requests.get")
def test_get_historical_data_success(mock_get, interactor):
    # Mocking a successful API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"code":"0", "msg": "","data": sample_candle_data}
    mock_get.return_value = mock_response

    result_data = interactor.get_historical_data(instrument, interval, from_date, to_date)

    # Assertions
    assert isinstance(result_data, dict)
    assert len(result_data) == 2  # since we provided 2 candles
    assert list(result_data.values())[0] == 16850.0  # Close price of first candle


@patch("requests.get")
def test_get_historical_data_api_error(mock_get, interactor):
    # Mocking an API error response
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    result = interactor.get_historical_data(instrument, interval, from_date, to_date)

    # Assertions
    assert result["statusCode"] == 500
    assert result["msg"] == "Error fetching data"


@patch("src.interactor.okx_interactor.OkxInteractor.get_historical_data")
def test_get_multiple_historical_data_success(mock_get_historical_data, interactor):
    # Mocking multiple successful data responses
    mock_get_historical_data.return_value = {
        datetime(2024, 1, 1, 0, 0): [16850.0],
        datetime(2024, 1, 1, 1, 0): [16950.0]
    }

    instruments = ["BTC-USDT", "ETH-USDT"]
    result = interactor.get_multiple_historical_data(instruments, interval, from_date, to_date)

    # Assertions
    assert isinstance(result, dict)
    assert "BTC-USDT" in result
    assert "ETH-USDT" in result
    assert len(result["BTC-USDT"]) == 2


@patch("src.interactor.okx_interactor.OkxInteractor.get_historical_data")
def test_get_multiple_historical_data_with_error(mock_get_historical_data, interactor):
    # Mocking one successful and one failed data response
    mock_get_historical_data.side_effect = [
        {datetime(2023, 1, 1, 0, 0): [16850.0]},  # First instrument successful
        Exception("API call failed")  # Second instrument fails
    ]

    instruments = ["BTC-USDT", "ETH-USDT"]
    result = interactor.get_multiple_historical_data(instruments, interval, from_date, to_date)

    # Assertions
    assert isinstance(result, dict)
    assert "BTC-USDT" in result
    assert "ETH-USDT" in result
    assert result["BTC-USDT"]  # BTC-USDT should have data
    assert result["ETH-USDT"] == []  # ETH-USDT should be empty due to error