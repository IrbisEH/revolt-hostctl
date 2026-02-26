from revolt_hostctl.core.models import Host, Network


def network_objects_generator(count):
    for i in range(count):
        name = f"{Network.__name__}{i}"
        cidr = f"10.0.0.0/{i}"
        yield Network(name=name, cidr=cidr)

def host_object_generator(count):
    for i in range(count):
        name = f"{Host.__name__}{i}"
        mac_address = f"00:00:00:00:00:h{i}"
        yield Host(name=name, mac_address=mac_address)
