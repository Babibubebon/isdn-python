from typing import Iterator

import requests

from . import __version__
from .model import ISDNRecord, ISDNRoot
from .parser import ISDNJpSitemapXMLParser

ISDN_XML_ENDPOINT = "https://isdn.jp/xml/{isdn}"
ISDN_IMAGE_ENDPOINT = "https://isdn.jp/images/thumbs/{isdn}.png"
ISDN_SITEMAP = "https://isdn.jp/sitemap.xml"


class ISDNClient:
    def __init__(
        self,
        xml_endpoint_url: str = ISDN_XML_ENDPOINT,
        image_endpoint_url: str = ISDN_IMAGE_ENDPOINT,
        sitemap_url: str = ISDN_SITEMAP,
    ):
        self.xml_endpoint_url = xml_endpoint_url
        self.image_endpoint_url = image_endpoint_url
        self.sitemap_url = sitemap_url
        self.s = requests.Session()
        self.set_user_agent(f"isdn-python/{__version__}")

    def set_user_agent(self, user_agent: str):
        self.s.headers.update({"user-agent": user_agent})

    @staticmethod
    def normalize_isdn(isdn: str) -> str:
        return isdn.replace("-", "").strip()

    def _get(self, isdn: str, endpoint_url: str) -> requests.Response:
        r = self.s.get(endpoint_url.format(isdn=self.normalize_isdn(isdn)))
        r.raise_for_status()
        return r

    def get(self, isdn: str) -> ISDNRecord:
        r = self._get(isdn, self.xml_endpoint_url)
        return ISDNRoot.from_xml_first(r.content)

    def get_raw(self, isdn: str) -> bytes:
        r = self._get(isdn, self.xml_endpoint_url)
        return r.content

    def get_image(self, isdn: str) -> bytes:
        r = self._get(isdn, self.image_endpoint_url)
        return r.content

    def _list(self) -> requests.Response:
        r = self.s.get(self.sitemap_url, stream=True)
        r.raise_for_status()
        return r

    def list(self) -> Iterator[str]:
        r = self._list()
        return ISDNJpSitemapXMLParser.parse_list(r.raw)
