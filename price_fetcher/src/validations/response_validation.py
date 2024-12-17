"""
This is the validation file to validate the response receive from the source
"""


def run_get_historical_response_validation(data, **expectation)-> None:
    """
    This is function runs multiple validation together
    Args:
        data:
        **expectation:

    Returns: None

    """

    assert validate_close_price_none_data(data)
    assert validate_missing_data(data, expectation["num_of_days"])


def validate_missing_data(data, expected_days)->bool:
    """
    This function will check if the lenght of data is received is same as data asked for days.
    expected value will be differ in different sceanrio, like 1hr, 4hr interval
    Args:
        data: data to be validated

    Returns: True if its is valid, otherwise False

    """

    return True if len(data)==expected_days else False


def validate_close_price_none_data(data)-> bool:
    """
    Function to validate if any value in close price is none
    data: data to be validated
    Returns: True if its is valid, otherwise False

    """
    for candle in data:
        if candle[4] is None:
            return False

    return True