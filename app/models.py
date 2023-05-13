from pydantic import BaseModel


class SearchParams(BaseModel):
    category: str
    brand: str
    word_to_search: str
