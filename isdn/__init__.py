import importlib.metadata

__version__ = importlib.metadata.version("isdn")


class InvalidIsdnError(ValueError):
    pass


from .client import ISDNClient
from .model import ISDN, ISDNRecord
