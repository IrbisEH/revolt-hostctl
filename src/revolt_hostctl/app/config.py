from pathlib import Path
from platformdirs import user_data_dir


class Config:
    def __init__(self) -> None:
        self.app_name = "revolt-hostctl"
        self.app_root = Path(user_data_dir(self.app_name))

        self.storage_dir = self.app_root / "storage"
        self.log_dir = self.app_root / "logs"

        self.log_level = "debug"
        self.log_max_bytes = 1024 * 1024 * 5
        self.log_backup_count = 5
        self.log_console = True
