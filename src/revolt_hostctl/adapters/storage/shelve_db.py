import shelve
from pathlib import Path


class ShelveAdapter:
    def __init__(self, storage_dir: Path):
        self.data = None
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.db_file = self.storage_dir / "shelve_data.db"

    def __enter__(self):
        if self.data is None:
            self.data = shelve.open(str(self.db_file), flag="c")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.data is not None:
            self.data.close()
            self.data = None

    def _ensure_open(self):
        if self.data is None:
            raise Exception('ShelveAdapter is not opened')

    def get(self, key):
        self._ensure_open()
        return self.data.get(key)

    def set(self, key, value):
        self._ensure_open()
        self.data[key] = value
