import uuid
import time
from pprint import pformat
from typing import Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _ts_now() -> int:
    return int(time.time())

@dataclass
class BaseModel:
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    created_at: int = field(default_factory=_ts_now)
    updated_at: int = field(default_factory=_ts_now)

    @property
    def storage_key(self) -> str:
        return self.__class__.__name__.lower()

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    def get_table_row(self, fields: Optional[list] = None) -> list:
        fields = fields or []
        date_fields = ["created_at", "updated_at"]

        def _format(_val):
            if isinstance(_val, int):
                date = datetime.fromtimestamp(_val)
                return date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return ""

        res = []
        for f in fields:
            val = getattr(self, f, "Unknown")
            if f in date_fields and isinstance(val, int):
                val = _format(val)

            res.append(val)

        return res

    def __repr__(self) -> str:
        props = [f"{k}={v!r}" for k, v in self.__dict__.items()]
        return f"{self.__class__.__name__}({' '.join(props)})"

    def __str__(self) -> str:
        return pformat(self.to_dict())


@dataclass
class Network(BaseModel):
    name: str | None = None
    cidr: str | None = None


@dataclass
class Host(BaseModel):
    name: str | None = None
    mac_address: str | None = None
    ip_addresses: set | None = None

    # metadata
    os: str | None = None
    os_version: str | None = None
    description: str | None = None
