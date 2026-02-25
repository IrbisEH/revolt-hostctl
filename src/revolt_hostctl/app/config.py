from pathlib import Path


class Config:
    APP_NAME = "revolt-hostctl"
    def __init__(self, app_root: Path):
        self.app_root = app_root
        self.storage_dir = app_root / "storage"
