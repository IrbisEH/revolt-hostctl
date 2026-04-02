from revolt_hostctl.app.utils import to_snake
import uuid
import time
import hashlib
from pathlib import Path
from typing import Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field, fields


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _ts_now() -> int:
    return int(time.time())


def _generate_deterministic_id(data: dict, fields: list[str]) -> str:
    values = []
    for f in fields:
        val = data.get(f)
        if val is None:
            val = ""
        values.append(str(val))
    joined = "|".join(values)
    return hashlib.md5(joined.encode()).hexdigest()


@dataclass(kw_only=True)
class BaseModel:
    id: str = field(default=None)
    created_at: int = field(default_factory=_ts_now)
    updated_at: int = field(default_factory=_ts_now)

    def __post_init__(self):
        if self.id is None:
            unique_fields = getattr(self, "__unique_fields__", None)
            if unique_fields:
                self.id = _generate_deterministic_id(self.__dict__, unique_fields)
            else:
                self.id = uuid.uuid4().hex

    @property
    def storage_key(self) -> str:
        return to_snake(self.__class__.__name__)

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


@dataclass(kw_only=True)
class Network(BaseModel):
    name: str
    cidr: str
    __unique_fields__ = ["name", "cidr"]


@dataclass(kw_only=True)
class IpAddress(BaseModel):
    address: str
    network: Network
    __unique_fields__ = ["address", "network"]


@dataclass(kw_only=True)
class Host(BaseModel):
    name: str
    mac_address: str | None = None
    ip_addresses: set | None = None

    # metadata
    os: str | None = None
    os_version: str | None = None
    description: str | None = None

    __unique_fields__ = ["name", "mac_address"]


@dataclass(kw_only=True)
class LocalVm(Host):
    vm_dir: Path
    __unique_fields__ = ["name", "mac_address", "vm_dir"]
