import importlib.metadata
import re
from dataclasses import asdict, dataclass, field
from datetime import date

__version__ = importlib.metadata.version("isdn")


class IsdnError(Exception):
    pass


class InvalidIsdnError(IsdnError):
    pass


@dataclass
class ISDN:
    code: str
    prefix: str | None = None
    group: str | None = None
    registrant: str | None = None
    publication: str | None = None
    check_digit: str | None = None

    @property
    def parts(self) -> list[str | None]:
        self.code = self.normalize(self.code)
        return [self.prefix, self.group, self.registrant, self.publication, self.check_digit]

    def __post_init__(self):
        if all(self.parts) and self.code != "".join(self.parts):
            raise ValueError(f"ISDNs of arguments do not match: {self.code} != {''.join(self.parts)}")

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

    @staticmethod
    def normalize(isdn: int | str) -> str:
        return str(isdn).replace("-", "").strip()

    @staticmethod
    def calc_check_digit(isdn: str) -> str:
        isdn = [int(n) for n in isdn]
        cd = 10 - (sum([(n if i % 2 == 0 else n * 3) for i, n in enumerate(isdn[:12])]) % 10)
        return str(cd % 10)

    @classmethod
    def from_disp_isdn(cls, disp_isdn: str) -> "ISDN":
        parts = disp_isdn.lstrip("ISDN").split("-")
        isdn = "".join(parts)
        if len(parts) != 5:
            raise InvalidIsdnError("ISDN must have 5 parts")
        return cls(isdn, *parts)


@dataclass
class UserOption:
    property: str
    value: str


@dataclass
class ExternalLink:
    uri: str
    title: str | None


@dataclass
class ISDNRecord:
    isdn: ISDN
    disp_isdn: str
    region: str
    class_: str
    type: str
    rating_gender: str
    rating_age: str
    product_name: str
    product_yomi: str | None
    publisher_code: str
    publisher_name: str
    publisher_yomi: str | None
    issue_date: date
    genre_code: str | None
    genre_name: str | None
    genre_user: str | None
    c_code: str | None
    author: str | None
    shape: str | None
    contents: str | None
    price: int | None
    price_unit: str | None
    barcode2: str | None
    product_comment: str | None
    product_style: str | None
    product_size: str | None
    product_capacity: int | None
    product_capacity_unit: str | None
    sample_image_uri: str
    useroption: list[UserOption] = field(default_factory=list)
    external_link: list[ExternalLink] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


from .client import ISDNClient
