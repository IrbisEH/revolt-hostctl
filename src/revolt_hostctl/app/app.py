from pathlib import Path
from importlib.metadata import version, PackageNotFoundError
from revolt_hostctl.app.config import Config
from revolt_hostctl.app.logger import Logger
from revolt_hostctl.adapters.storage.shelve_db import ShelveAdapter
from revolt_hostctl.core.storage import Storage


class App:
    def __init__(self, root_dir: Path):
        self.config = Config(root_dir)
        self.logger = Logger(self.config)
        self.adapter = ShelveAdapter(self.config.storage_dir)
        self.storage = Storage(self.adapter)

    def get_version(self) -> str:
        try:
            return version(self.config.app_name)
        except PackageNotFoundError:
            return "0.0.0+dev"
