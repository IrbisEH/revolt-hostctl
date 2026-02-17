from src.revolt_hostctl.adapters.storage.shelve_db import ShelveAdapter
from src.revolt_hostctl.core.storage import Storage
from src.revolt_hostctl.core.models import Network, Host


def main():
    adapter = ShelveAdapter()
    storage = Storage(adapter)
    storage.load_state()

    print(storage.hosts)
    print(storage.networks)

    net = Network(
        name="private_vpn",
        cidr="10.0.0.0/16"
    )

    host = Host(
        name="dpiui2",
        mac_address="00:11:22:33:44:55"
    )



    storage.add_network(net)
    storage.add_host(host)

    storage.save_state()

