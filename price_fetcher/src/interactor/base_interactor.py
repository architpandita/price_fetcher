
class BaseInteractor:
    """
    This is Base class, all common feature should be here to control the class design
    """
    def __init__(self, **kwargs):
        pass

    def get_current_price(self, instrument, price):
        raise NotImplementedError

    @staticmethod
    def _conf():
        raise NotImplementedError

    def get_historical_data(self, instruments: str, tick_size: str, from_date:str, to_date: str)-> dict:
        raise NotImplementedError