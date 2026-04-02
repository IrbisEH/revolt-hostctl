import os
from dotenv import load_dotenv
from pathlib import Path
from platformdirs import user_data_dir


class Config:
    def __init__(self) -> None:
        self.app_name = "revolt-hostctl"
        self.app_root = Path(user_data_dir(self.app_name))

        self.storage_dir = self.app_root / "storage"
        self.log_dir = self.app_root / "logs"
        self.env_file = self.app_root / ".env"

        self.env_file.touch(exist_ok=True)

        load_dotenv(str(self.env_file))

        self.log_level = os.getenv("LOG_LEVEL", "DEBUG")
        self.log_max_bytes = int(os.getenv("LOG_MAX_BYTES", 1024 * 1024 * 5))
        self.log_backup_count = int(os.getenv("LOG_BACKUP_COUNT", 5))
        self.log_console = bool(os.getenv("LOG_CONSOLE", 0))
