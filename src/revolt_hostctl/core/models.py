import uuid
from datetime import datetime, timezone
from typing import List, Optional
from dataclasses import dataclass, field


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Network:
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    name: Optional[str] = None
    cidr: Optional[str] = None
    storage_key = "network"


    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "cidr": self.cidr
        }


@dataclass
class Host:
    # required
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    name: str = ""
    mac_address: str = ""

    # optional
    ip_addresses: List[str] = field(default=list)

    # metadata
    os: Optional[str] = None
    os_version: Optional[str] = None
    description: Optional[str] = None

    created_at: datetime = field(default_factory=_utcnow)
    updated_at: datetime = field(default_factory=_utcnow)

    storage_key = "host"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "mac_address": self.mac_address,
            "ip_addresses": self.ip_addresses,
            "os": self.os,
            "os_version": self.os_version,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __str__(self):
        return f"revolt {self.name} host"

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
