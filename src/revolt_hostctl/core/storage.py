from revolt_hostctl.core.models import Network, Host


class Storage:
    CLASS_MAP = {'network': Network,'host': Host}
    COLLECTIONS = tuple(CLASS_MAP.keys())

    def __init__(self, adapter):
        self.adapter = adapter

        for attr_key in self.COLLECTIONS:
            setattr(self, attr_key, dict())

    def load_state(self) -> None:
        with self.adapter as db:
            for attr_key in self.COLLECTIONS:
                klass = self.CLASS_MAP[attr_key]
                data = db.get(attr_key)

                if isinstance(data, list):
                    objs = [klass(**i) for i in data]
                    collection = {obj.id: obj for obj in objs}
                    setattr(self, attr_key, collection)

    def save_state(self) -> None:
        with self.adapter as db:
            for attr_key in self.COLLECTIONS:
                data = [i.to_dict() for i in getattr(self, attr_key).values()]
                db.set(attr_key, data)

    def add(self, obj: Network | Host) -> None:
        self.valid_obj(obj)
        data = getattr(self, obj.storage_key)
        data[obj.id] = obj

    def get(self, obj_type: str, obj_id: str):
        obj_type = obj_type.lower()
        self.valid_type(obj_type)
        data = getattr(self, obj_type)
        return data.get(obj_id)

    def list(self, obj_type: str):
        obj_type = obj_type.lower()
        self.valid_type(obj_type)
        data = getattr(self, obj_type)
        return list(data.values())

    def update(self, obj):
        self.add(obj)

    def remove(self, obj):
        self.valid_obj(obj)
        data = getattr(self, obj.storage_key)
        return data.pop(obj.id, None)

    @staticmethod
    def valid_obj(obj):
        check = [
            isinstance(obj, Network),
            isinstance(obj, Host)
        ]

        if not any(check):
            raise ValueError(f"Invalid storage type: {type(obj)}")

    def valid_type(self, obj_type):
        if obj_type not in self.COLLECTIONS:
            raise ValueError(f"Invalid storage type: {obj_type}")
