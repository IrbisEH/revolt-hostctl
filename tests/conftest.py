import pytest
from pathlib import Path


class FakeConfig:
    def __init__(self, root: Path):
        self.app_name = "test-app"
        self.app_root = root

        self.storage_dir = self.app_root / "storage"
        self.log_dir = self.app_root / "logs"

        self.log_level = "debug"
        self.log_max_bytes = 1024 * 1024 * 5
        self.log_backup_count = 5
        self.log_console = True


@pytest.fixture
def fake_config(tmp_path):
    return FakeConfig(tmp_path)
