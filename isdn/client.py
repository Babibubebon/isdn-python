from typing import Iterator

import requests

from . import ISDNRecord, __version__
from .parser import ISDNJpXMLParser

ISDN_API_ENDPOINT = "https://isdn.jp/xml/"
ISDN_SITEMAP = "https://isdn.jp/sitemap.xml"


class ISDNClient:
    def __init__(self, endpoint_url: str = ISDN_API_ENDPOINT, sitemap_url: str = ISDN_SITEMAP):
        self.endpoint_url = endpoint_url
        self.sitemap_url = sitemap_url
        self.s = requests.Session()
        self.set_user_agent(f"isdn-python/{__version__}")

    def set_user_agent(self, user_agent: str):
        self.s.headers.update({"user-agent": user_agent})

    @staticmethod
    def normalize_isdn(isdn: str) -> str:
        return isdn.replace("-", "").strip()

    def _get(self, isdn: str) -> requests.Response:
        r = self.s.get(self.endpoint_url + self.normalize_isdn(isdn))
        r.raise_for_status()
        return r

    def get(self, isdn: str) -> ISDNRecord:
        r = self._get(isdn)
        return ISDNJpXMLParser.parse_record(r.content)

    def get_raw(self, isdn: str) -> bytes:
        r = self._get(isdn)
        return r.content

    def _list(self) -> requests.Response:
        r = self.s.get(self.sitemap_url, stream=True)
        r.raise_for_status()
        return r

    def list(self) -> Iterator[str]:
        r = self._list()
        return ISDNJpXMLParser.parse_list(r.raw)
