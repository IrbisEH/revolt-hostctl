from pathlib import Path


class Config:
    def __init__(self, app_root: Path):
        self.app_root = app_root
        self.app_name = "revolt-hostctl"
        self.storage_dir = app_root / "storage"
        self.log_dir = app_root / "logs"
        self.log_level = "debug"
        self.log_max_bytes = 1024 * 1024 * 5
        self.log_backup_count = 5
        self.log_console = True
