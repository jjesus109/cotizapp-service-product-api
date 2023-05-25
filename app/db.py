from app.errors import DBConnectionError

import motor.motor_asyncio
from pymongo.errors import (
    ConfigurationError,
    ConnectionFailure,
)


class DBConnection:

    def __init__(self, url_connection: str) -> None:
        try:
            client = motor.motor_asyncio.AsyncIOMotorClient(url_connection)
        except (ConfigurationError, ConnectionFailure) as e:
            raise DBConnectionError(
                f"Could not connect to database due to: {e}"
            )
        self.db = client.business
