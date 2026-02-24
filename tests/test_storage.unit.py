import pytest

from revolt_hostctl.core.storage import Storage
from revolt_hostctl.core.models import Host, Network


class InMemoryAdapter:
    """Fake adapter for in-memory storage"""
    def __init__(self):
        self._data = {}
        self._opened = False

    def __enter__(self):
        self._opened = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._opened = False

    def get(self, key):
        assert self._opened
        return self._data.get(key)

    def set(self, key, value):
        assert self._opened
        self._data[key] = value


def test_storage_add_get_remove_host():
    storage = Storage(InMemoryAdapter())
    h = Host(name="h1", mac_address="aa:bb:cc:dd:ee:ff")

    storage.add(h)
    resp = storage.get("hosts", h._id)
    assert resp is h

    removed = storage.remove("hosts", h._id)
    assert removed is h

    resp = storage.get("hosts", h._id)
    assert resp is None


def test_storage_list_returns_values_view():
    storage = Storage(InMemoryAdapter())
    n1 = Network(name="net1", cidr="10.0.0.0/24")
    n2 = Network(name="net2", cidr="10.0.1.0/24")

    storage.add("networks", n1)
    storage.add("networks", n2)

    items = storage.list("networks")
    assert isinstance(items, list)
    assert set(x._id for x in items) == {n1._id, n2._id}


@pytest.mark.parametrize("bad_type", [None, 123, "host", "NETWORKS", ""])
def test_storage_invalid_type_raises(bad_type):
    storage = Storage(InMemoryAdapter())
    with pytest.raises(ValueError):
        storage.list(bad_type)


def test_storage_invalid_class_raises():
    storage = Storage(InMemoryAdapter())
    with pytest.raises(ValueError):
        storage.add("networks", Host(name="h1", mac_address="aa"))
