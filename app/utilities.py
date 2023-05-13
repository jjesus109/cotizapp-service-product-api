from app.config import Config
from app.errors import TokenError

import requests


URL = "https://developers.syscom.mx/oauth/token"
config = Config()


def get_token() -> str:
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = f"client_id={config.client_id}&client_secret={config.client_secret}&grant_type=client_credentials"  # noqa
    try:
        response = requests.post(URL, headers=headers, data=data)
        response.raise_for_status()
    except Exception:
        raise TokenError("Problems while getting acces token")
    data = response.json()
    access_token = data.get("access_token")
    if access_token:
        return access_token
    raise TokenError("Problems while getting acces token")
