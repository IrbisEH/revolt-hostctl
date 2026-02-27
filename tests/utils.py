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

def is_value_err(func, args):
    value_err = False
    try:
        func(args)
    except ValueError:
        value_err = True
    return value_err



def try_func(func, *args, **kwargs):
    try:
        res = func(*args, **kwargs)
    except Exception as e:
        return None, e
    return res, None