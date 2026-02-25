from pathlib import Path
from revolt_hostctl.app.config import Config
from revolt_hostctl.adapters.storage.shelve_db import ShelveAdapter
from revolt_hostctl.core.storage import Storage


class App:
    def __init__(self, root_dir: Path):
        self.config = Config(root_dir)
        self.adapter = ShelveAdapter(self.config.storage_dir)
        self.storage = Storage(self.adapter)

    def get_version(self):
        return self.config.app_version
    