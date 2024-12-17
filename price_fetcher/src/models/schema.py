from pydantic import BaseModel
from typing import Dict


class PriceData(BaseModel):
    """
    This is schema for the response data for single instrument
    """
    code: str
    msg: str
    data: list
