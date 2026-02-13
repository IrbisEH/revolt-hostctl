class Storage:
    def __init__(self, adapter):
        self.adapter = adapter
        self.hosts = dict()
        self.networks = dict()

    def load_state(self):
        pass

    def save_state(self):
        pass

    def list_hosts(self):
        pass

    def get_host(self, *args, **kwargs):
        pass

    def add_host(self, *args, **kwargs):
        pass

    def update_host(self, *args, **kwargs):
        pass

    def remove_host(self, *args, **kwargs):
        pass

    def list_networks(self, *args, **kwargs):
        pass

    def get_network(self, *args, **kwargs):
        pass

    def add_network(self, *args, **kwargs):
        pass

    def update_network(self, *args, **kwargs):
        pass

    def remove_network(self, *args, **kwargs):
        pass
