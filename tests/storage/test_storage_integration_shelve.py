from tests.utils import network_objects_generator, host_object_generator
from revolt_hostctl.core.storage import Storage
from revolt_hostctl.adapters.storage.shelve_db import ShelveAdapter



def test_storage_save_load_roundtrip(tmp_path):
    adapter = ShelveAdapter(tmp_path)
    storage = Storage(adapter)

    obj_lists = [
        [i for i in network_objects_generator(10)],
        [i for i in host_object_generator(10)]
    ]

    obj_types = []

    for objects in obj_lists:
        obj_types.append(type(objects[0]))

        for obj in objects:
            storage.add(obj)

    storage.save_state()
    storage.load_state()

    for obj_type in obj_types:
        obj_type_name = obj_type.__name__
        obj_list = storage.list(obj_type_name)

        assert len(obj_list) == 10
        assert all(isinstance(obj, obj_type) for obj in obj_list)

    for objects in obj_lists:
        for obj in objects:
            obj_type_name = obj.__class__.__name__
            resp = storage.get(obj_type_name, obj.id)

            assert isinstance(resp, type(obj))

            for prop_name in obj.__dict__.keys():
                obj_attr = getattr(obj, prop_name)
                resp_attr = getattr(resp, prop_name)
                assert obj_attr == resp_attr
