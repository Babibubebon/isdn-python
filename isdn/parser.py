import re
from typing import IO, Iterator

from lxml import etree

from . import ISDN, ExternalLink, ISDNRecord, UserOption

namespaces = {"isdn": "https://isdn.jp/schemas/0.1", "sitemap": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class ISDNJpXMLParser:
    @staticmethod
    def convert_tag_name(tag: str) -> str:
        key = etree.QName(tag).localname.replace("-", "_")
        if key == "class":
            key += "_"
        return key

    @staticmethod
    def parse_value(elem: etree.Element, key: str) -> str | UserOption | ExternalLink:
        data = dict()
        for child in elem:
            data[ISDNJpXMLParser.convert_tag_name(child.tag)] = child.text

        match key:
            case "useroption":
                return UserOption(**data)
            case "external_link":
                return ExternalLink(**data)
            case _:
                return elem.text

    @staticmethod
    def parse_record(doc: str | bytes) -> ISDNRecord:
        root = etree.fromstring(doc)
        item = root.find("./isdn:item", namespaces=namespaces)
        data = dict()
        for child in item:
            key = ISDNJpXMLParser.convert_tag_name(child.tag)
            value = ISDNJpXMLParser.parse_value(child, key)

            if key in {"useroption", "external_link"}:
                if key not in data:
                    data[key] = []
                data[key].append(value)
            else:
                data[key] = value

        return ISDNRecord(isdn=ISDN.from_disp_isdn(data["disp_isdn"]), **data)

    @staticmethod
    def parse_list(file: str | IO) -> Iterator[str]:
        for event, elm in etree.iterparse(
            file, events=("end",), tag=[f"{{{namespaces['sitemap']}}}loc"], remove_blank_text=True
        ):
            m = re.match("https://isdn.jp/(\d{13})", elm.text)
            if not m:
                continue
            yield m.group(1)
