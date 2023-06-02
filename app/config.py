from pydantic import BaseSettings


class Config(BaseSettings):
    syscom_api_url: str
    syscom_token_url: str
    client_id: str
    client_secret: str
    mongodb_url: str
    mongo_db: str
    stream_consume: bool
    kafka_server: str
    kafka_protocol: str
    sasl_mechanism: str
    sasl_username: str
    sasl_pass: str
    max_search_elements: int
