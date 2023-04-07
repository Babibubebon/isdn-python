import re
from datetime import date
from decimal import Decimal

from pydantic import Field, HttpUrl, root_validator, validator
from pydantic.dataclasses import dataclass
from pydantic_xml import BaseXmlModel, element

from . import InvalidIsdnError

NSMAP = {"": "https://isdn.jp/schemas/0.1"}


@dataclass
class ISDN:
    code: str
    prefix: str | None = None
    group: str | None = None
    registrant: str | None = None
    publication: str | None = None
    check_digit: str | None = None

    @root_validator(pre=True)
    def validate_code(cls, values):
        code = str(values["code"])

        if code.startswith("ISDN") and "-" in code:
            parts = code.lstrip("ISDN").split("-")
            code = "".join(parts)
            if len(parts) != 5:
                raise InvalidIsdnError("ISDN must have 5 parts")

            values.update(
                {
                    "prefix": parts[0],
                    "group": parts[1],
                    "registrant": parts[2],
                    "publication": parts[3],
                    "check_digit": parts[4],
                }
            )
        else:
            code = cls.normalize(code)

        arg_parts = [values.get(k) for k in ["prefix", "group", "registrant", "publication", "check_digit"]]
        if all(arg_parts) and code != "".join(arg_parts):
            raise ValueError(f"ISDNs of arguments do not match: {code} != {''.join(arg_parts)}")

        return values | {"code": code}

    @property
    def parts(self) -> list[str | None]:
        self.code = self.normalize(self.code)
        return [self.prefix, self.group, self.registrant, self.publication, self.check_digit]

    @staticmethod
    def normalize(isdn: int | str) -> str:
        return str(isdn).replace("-", "").strip()

    @staticmethod
    def calc_check_digit(isdn: str) -> str:
        isdn = [int(n) for n in isdn]
        cd = 10 - (sum([(n if i % 2 == 0 else n * 3) for i, n in enumerate(isdn[:12])]) % 10)
        return str(cd % 10)

    def to_disp_isdn(self) -> str | None:
        if not all(self.parts):
            return None
        return f"ISDN{self.prefix}-{self.group}-{self.registrant}-{self.publication}-{self.check_digit}"

    def validate(self, raise_error: bool = False) -> bool:
        if not re.fullmatch(r"\d+", self.code):
            if raise_error:
                raise InvalidIsdnError("Contains non-numeric characters")
            else:
                return False
        if len(self.code) != 13:
            if raise_error:
                raise InvalidIsdnError("ISDN must be 13 digits")
            else:
                return False
        if not (self.code.startswith("278") or self.code.startswith("279")):
            if raise_error:
                raise InvalidIsdnError("ISDN prefix must be 278 or 279")
            else:
                return False
        if self.calc_check_digit(self.code) != self.code[12]:
            if raise_error:
                raise InvalidIsdnError("Invalid check digit")
            else:
                return False

        # Validate parts
        if self.group and not (1 <= len(self.group) <= 5):
            if raise_error:
                raise InvalidIsdnError("Group part must be 1 to 5 digits")
            else:
                return False
        if self.registrant and not (1 <= len(self.registrant) <= 7):
            if raise_error:
                raise InvalidIsdnError("Publisher part must be 1 to 7 digits")
            else:
                return False
        if self.publication and not (1 <= len(self.publication) <= 2):
            if raise_error:
                raise InvalidIsdnError("Publication part must be 1 to 2 digits")
            else:
                return False

        return True


class UserOption(BaseXmlModel, tag="useroption", nsmap=NSMAP):
    property: str = element(tag="property", default="")
    value: str = element(tag="value", default="")


class ExternalLink(BaseXmlModel, tag="external-link", nsmap=NSMAP):
    title: str | None = element(tag="title")
    uri: HttpUrl = element(tag="uri")


class ISDNRecord(BaseXmlModel, nsmap=NSMAP):
    isdn: ISDN = element(tag="disp-isdn")
    region: str = element(tag="region")
    class_: str = element(tag="class")
    type: str = element(tag="type")
    rating_gender: str = element(tag="rating_gender")
    rating_age: str = element(tag="rating_age")
    product_name: str = element(tag="product-name")
    product_yomi: str | None = element(tag="product-yomi")
    publisher_code: str = element(tag="publisher-code")
    publisher_name: str = element(tag="publisher-name")
    publisher_yomi: str | None = element(tag="publisher-yomi")
    issue_date: date = element(tag="issue-date")
    genre_code: str | None = element(tag="genre-code")
    genre_name: str | None = element(tag="genre-name")
    genre_user: str | None = element(tag="genre-user")
    c_code: str | None = element(tag="c-code")
    author: str | None = element(tag="author")
    shape: str | None = element(tag="shape")
    contents: str | None = element(tag="contents")
    price: Decimal | None = element(tag="price")
    price_unit: str | None = element(tag="price-unit")
    barcode2: str | None = element(tag="barcode2")
    product_comment: str | None = element(tag="product-comment")
    product_style: str | None = element(tag="product-style")
    product_size: str | None = element(tag="product-size")
    product_capacity: Decimal | None = element(tag="product-capacity")
    product_capacity_unit: str | None = element(tag="product-capacity-unit")
    sample_image_uri: HttpUrl | None = element(tag="sample-image-uri")
    useroptions: list[UserOption] = Field(default_factory=list)
    external_links: list[ExternalLink] = Field(default_factory=list)

    @validator("isdn", pre=True)
    def parse_disp_isdn(cls, isdn: str) -> ISDN:
        return ISDN(code=isdn)


class ISDNRoot(BaseXmlModel, tag="isdn", nsmap=NSMAP):
    records: list[ISDNRecord] = element(tag="item")

    @classmethod
    def from_xml_first(cls, source: str | bytes) -> ISDNRecord:
        isdn_root = cls.from_xml(source)
        return isdn_root.records[0]
