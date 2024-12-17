import pytest
from src.errors.api_error import (
    LoginError,
    MissingDateError,
    InvalidInputError,
    NoDataFoundError,
    CustomError,
    InvalidResponseError
)


def test_login_error():
    with pytest.raises(LoginError, match="Error: while logging"):
        raise LoginError("Error: while logging")


def test_invalid_response_error():
    with pytest.raises(InvalidResponseError, match="Error: invalid response got from external api"):
        raise InvalidResponseError("Error: invalid response got from external api")


def test_missing_date_error():
    with pytest.raises(MissingDateError, match="Error: Date is missing"):
        raise MissingDateError("Error: Date is missing")


def test_invalid_input_error():
    with pytest.raises(InvalidInputError, match="Error: input value given is not correct please check."):
        raise InvalidInputError("Error: input value given is not correct please check.")


def test_no_data_found_error():
    with pytest.raises(NoDataFoundError, match="Error: no data is received."):
        raise NoDataFoundError("Error: no data is received.")


def test_custom_error():
    with pytest.raises(CustomError, match="Error: Custom error for multipurpose usage"):
        raise CustomError("Error: Custom error for multipurpose usage")
