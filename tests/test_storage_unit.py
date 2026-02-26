from revolt_hostctl.core.storage import Storage
from revolt_hostctl.core.models import Host, Network


class InMemoryAdapter:
    """Fake adapter for in-memory storage"""
    def __init__(self):
        self._data = {}
        self._opened = False

    def __enter__(self):
        self._opened = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._opened = False

    def get(self, key):
        assert self._opened
        return self._data.get(key)

    def set(self, key, value):
        assert self._opened
        self._data[key] = value


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

def test_storage_unit_add_get_remove_methods():
    adapter = InMemoryAdapter()
    storage = Storage(adapter)

    objects = [
        Network(name=f"{Network.__name__}1", cidr="10.0.0.0/24"),
        Host(name=f"{Host.__name__}1", mac_address="aa:bb:cc:dd:ee:ff")
    ]

    for obj in objects:
        storage.add(obj)

        resp = storage.get(obj.storage_key, obj.id)

        obj_type_name = obj.__class__.__name__
        resp_type_name = resp.__class__.__name__

        assert resp is not None
        assert resp_type_name == obj_type_name

        for prop_name in obj.__dict__.keys():
            obj_attr = getattr(obj, prop_name)
            resp_attr = getattr(resp, prop_name)
            assert obj_attr == resp_attr

        obj.name = f"{obj_type_name[0]}2"

        storage.update(obj)
        resp = storage.get(obj.storage_key, obj.id)

        assert resp is not None
        assert resp.name == obj.name

        storage.remove(obj)
        resp = storage.get(obj.storage_key, obj.id)

        assert resp is None

def test_storage_unit_save_load_list_methods():
    adapter = InMemoryAdapter()
    storage = Storage(adapter)

    generators = [
        network_objects_generator(10),
        host_object_generator(10)
    ]

    obj_types = []

    for genrtr in generators:
        objects = [i for i in genrtr]
        obj_types.append(type(objects[0]))

        for obj in objects:
            storage.add(obj)

    storage.save_state()
    storage.load_state()

    for obj_type in obj_types:
        obj_type_name = obj_type.__name__.lower()
        obj_list = storage.list(obj_type_name)

        assert len(obj_list) == 10
        assert all(isinstance(obj, obj_type) for obj in obj_list)
