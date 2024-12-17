
class LoginError(Exception):
    """
     Error: while logging
    """
    pass


class MissingDateError(Exception):
    """
     Error: Date is missing
    """
    pass


class InvalidInputError(Exception):
    """
     Error: input value given is not correct please check.
    """
    pass


class NoDataFoundError(Exception):
    """
     Error: no data is received.
    """
    pass


class InvalidResponseError(Exception):
    """
     Error: invalid data is received.
    """
    pass


class CustomError(Exception):
    """
     Error: Custom error for multipurpose usage
    """
    pass


