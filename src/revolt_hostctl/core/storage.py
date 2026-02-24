from revolt_hostctl.core.models import Network, Host


class Storage:
    CLASS_MAP = {'networks': Network,'hosts': Host}
    COLLECTORS = tuple(CLASS_MAP.keys())

    def __init__(self, adapter):
        self.adapter = adapter

        for attr_key in self.COLLECTORS:
            setattr(self, attr_key, dict())

    def load_state(self):
        with self.adapter as db:
            for attr_key in self.COLLECTORS:
                klass = self.CLASS_MAP[attr_key]
                data = db.get(attr_key)

                if isinstance(data, list):
                    objs = [klass(**i) for i in data]
                    collector = {obj._id: obj for obj in objs}
                    setattr(self, attr_key, collector)

    def save_state(self):
        with self.adapter as db:
            for attr_key in self.COLLECTORS:
                data = [i.to_dict() for i in getattr(self, attr_key).values()]
                db.set(attr_key, data)

    def list(self, _type):
        self._valid(_type)
        data = getattr(self, _type)
        return list(data.values())

    def get(self, _type, _id):
        self._valid(_type)
        data = getattr(self, _type)
        return data.get(_id)

    def add(self, _type, obj):
        self._valid(_type, obj)
        data = getattr(self, _type)
        data[obj._id] = obj

    def update(self, _type, obj):
        self.add(_type, obj)

    def remove(self, _type, _id):
        self._valid(_type)
        data = getattr(self, _type)
        return data.pop(_id, None)

    def _valid(self, _type, obj=None):
        self._valid_type(_type)
        if obj is not None:
            self._valid_class(_type, obj)

    def _valid_type(self, _type):
        if not isinstance(_type, str) or _type not in self.COLLECTORS:
            raise ValueError(f"Invalid storage type: {_type}")

    def _valid_class(self, _type, obj):
        klass = self.CLASS_MAP.get(_type)
        if klass is None or not isinstance(obj, klass):
            raise ValueError(f"Invalid storage class: {obj}")
