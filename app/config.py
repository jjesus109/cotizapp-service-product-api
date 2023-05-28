from pydantic import BaseSettings


class Config(BaseSettings):
    syscom_api_url: str
    client_id: str
    client_secret: str
    mongodb_url: str
