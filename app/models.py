from typing import Union
from pydantic import BaseModel


class SearchParams(BaseModel):
    category: str
    brand: str
    word_to_search: str


class ServiceModel(BaseModel):
    name: str
    description: str
    client_price: float
    real_price: float
    image: str


class ServiceUpdateModel(BaseModel):
    name: Union[str, None] = None
    description: Union[str, None] = None
    client_price: Union[float, None] = None
    real_price: Union[float, None] = None
    image: Union[str, None] = None
