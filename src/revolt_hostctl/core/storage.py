from src.revolt_hostctl.core.models import Network, Host


class Storage:
    COLLECTORS = ('networks', 'hosts')
    CLASS_MAP = {'networks': Network,'hosts': Host}

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

    def list_hosts(self):
        for item in self.hosts.values():
            yield item

    def get_host(self, _id=None):
        if _id is None:
            raise Exception('Invalid storage id')
        return self.hosts.get(_id)

    def add_host(self, obj=None):
        if obj is None or not isinstance(obj, Host):
            raise Exception('Invalid storage class')
        self.hosts[obj._id] = obj

    def update_host(self, obj=None):
        if obj is None or not isinstance(obj, Host):
            raise Exception('Invalid storage class')
        self.add_host(obj)

    def remove_host(self, _id=None):
        if _id is None:
            raise Exception('Invalid storage id')
        del self.hosts[_id]

    def list_networks(self):
        for item in self.networks.values():
            yield item

    def get_network(self, _id=None):
        if _id is None:
            raise Exception('Invalid storage id')
        return self.networks.get(_id)

    def add_network(self, obj=None):
        print(obj)
        print(type(obj))
        if obj is None or not isinstance(obj, Network):
            raise Exception('Invalid storage class')
        self.networks[obj._id] = obj

    def update_network(self, obj=None):
        if obj is None or not isinstance(obj, Network):
            raise Exception('Invalid storage class')
        self.add_network(obj)

    def remove_network(self, _id=None):
        if _id is None:
            raise Exception('Invalid storage id')
        del self.networks[_id]
