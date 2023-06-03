from typing import Optional, TypedDict

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


class ServiceDictModel(TypedDict):
    _id: str
    name: str
    description: str
    client_price: float
    real_price: float


class ProductModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    list_price: float
    discount_price: float
    image: str
    stock_number: int
    brand: str
    product_id: int
    model: str
    sat_key: int
    weight: float

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ProducDictModel(BaseModel):
    _id: str
    title: str
    list_price: float
    discount_price: float
    image: str
    stock_number: int
    brand: str
    product_id: int
    model: str
    sat_key: int
    weight: float


class ExistenceModel(TypedDict):
    nuevo: int
    asterisco: dict


class PreciosModel(TypedDict):
    precio_1: float
    precio_especial: float
    precio_descuento: float
    precio_lista: float


class ProductResponseSearchModel(TypedDict):
    producto_id: int
    modelo: str
    total_existencia: int
    titulo: str
    marca: str
    sat_key: int
    img_portada: str
    link_privado: str
    categorias: list
    pvol: float
    marca_logo: str
    link: str
    iconos: list
    peso: float
    existencia: ExistenceModel
    unidad_de_medida: dict
    alto: int
    largo: int
    ancho: int
    precios: PreciosModel
    pagina: int
    paginas: int
