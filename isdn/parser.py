import re
from typing import IO, Iterator

from lxml import etree

namespaces = {"sitemap": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class ISDNJpSitemapXMLParser:
    @staticmethod
    def parse_list(file: str | IO) -> Iterator[str]:
        for event, elm in etree.iterparse(
            file, events=("end",), tag=[f"{{{namespaces['sitemap']}}}loc"], remove_blank_text=True
        ):
            m = re.match(r"https://isdn.jp/(\d{13})", elm.text)
            if not m:
                continue
            yield m.group(1)
