from typing import Optional

from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class SearchParams(BaseModel):
    category: str
    brand: str
    word_to_search: str


class ServiceModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    description: str = Field(...)
    client_price: float = Field(...)
    real_price: float = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Mantenimiento",
                "description": "Mantenimiento preventivo y correctivo",
                "client_price": 522,
                "real_price": 200
            }
        }


class ServiceUpdateModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    client_price: Optional[float]
    real_price: Optional[float]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        sschema_extra = {
            "example": {
                "name": "Mantenimiento",
                "description": "Mantenimiento preventivo y correctivo",
                "client_price": 600,
                "real_price": 180
            }
        }
