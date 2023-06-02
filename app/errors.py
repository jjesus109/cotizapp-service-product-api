class TokenError(Exception):
    """When theres a problem getting acess token"""


class DBConnectionError(Exception):
    """When could not connect to database"""


class ElementNotFoundError(Exception):
    """When element not found in DB"""
