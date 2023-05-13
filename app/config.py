from pydantic import BaseSettings


class Config(BaseSettings):

    client_id: str
    client_secret: str
