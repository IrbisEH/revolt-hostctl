from pathlib import Path

from revolt_hostctl.core.storage import Storage
from revolt_hostctl.core.models import Host, Network
from revolt_hostctl.adapters.storage.shelve_db import ShelveAdapter


#TODO: refactor to use real pytest tmp paths
def test_storage_save_load_roundtrip(tmp_path: Path):
    adapter = ShelveAdapter(tmp_path / "db")
    storage = Storage(adapter)

    h = Host(name="h1", mac_address="aa:bb:cc", ip_addresses=["10.0.0.10"])
    n = Network(name="net1", cidr="10.0.0.0/24")

    storage.add("hosts", h)
    storage.add("networks", n)

    storage.save_state()

    storage2 = Storage(ShelveAdapter(tmp_path / "db"))
    storage2.load_state()

    h2 = storage2.get("hosts", h._id)
    n2 = storage2.get("networks", n._id)

    assert h2 is not None
    assert h2.name == "h1"
    assert h2.mac_address == "aa:bb:cc"
    assert h2.ip_addresses == ["10.0.0.10"]

    assert n2 is not None
    assert n2.cidr == "10.0.0.0/24"