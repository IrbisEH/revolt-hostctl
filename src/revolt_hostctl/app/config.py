from pathlib import Path


class Config:
    VERSION = "0.1.0"
    def __init__(self, app_root: Path):
        self.app_version = self.VERSION
        self.app_root = app_root
        self.storage_dir = app_root / "storage"
