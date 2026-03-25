import uuid
import time
from typing import Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field, fields


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

    def _ordered_items(self):
        data = {f.name: getattr(self, f.name) for f in fields(self)}

        keys = list(data.keys())
        keys.remove("id")
        keys.remove("created_at")
        keys.remove("updated_at")

        ordered_keys = ["id"] + keys + ["created_at", "updated_at"]

        return [(k, data[k]) for k in ordered_keys]

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    def get_table_row(self, _fields: Optional[list] = None) -> list:
        _fields = _fields or []
        date_fields = ["created_at", "updated_at"]

        def _format(_val):
            if isinstance(_val, int):
                date = datetime.fromtimestamp(_val)
                return date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return ""

        res = []
        for f in _fields:
            val = getattr(self, f, "Unknown")
            if f in date_fields and isinstance(val, int):
                val = _format(val)

            res.append(val)

        return res

    def __repr__(self) -> str:
        props = [f"{k}={v!r}" for k, v in self.__dict__.items()]
        return f"{self.__class__.__name__}({' '.join(props)})"

    def __str__(self) -> str:
        items = self._ordered_items()
        max_key_len = max(len(k) for k, _ in items)

        lines = []
        for key, value in items:
            value_str = "-" if value is None else str(value)
            lines.append(f"{key.ljust(max_key_len)} {value_str}")

        return "\n".join(lines)


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
