import uuid
from datetime import datetime, timezone
from typing import List, Optional
from dataclasses import dataclass, field


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Network:
    name: str
    cidr: str


@dataclass
class Host:
    # required
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)
    name: str = ""
    mac_address: str = ""

    # optional
    network: List[Network] = field(default=list)

    # metadata
    os: Optional[str] = None
    os_version: Optional[str] = None
    description: Optional[str] = None

    created_at: datetime = field(default_factory=_utcnow)
    updated_at: datetime = field(default_factory=_utcnow)

    def __str__(self):
        return f"revolt {self.name} host"

    # TODO: add Networks description if need
    def __repr__(self):
        return (f"Host("
                f"_id={self._id} "
                f"name={self.name} "
                f"mac_address={self.mac_address} "
                f"os={self.os} "
                f"os_version={self.os_version} "
                f"description={self.description}"
                f"created_at={self.created_at} "
                f"updated_at={self.updated_at}"
                f")")
