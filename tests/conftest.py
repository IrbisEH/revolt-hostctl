import pytest
from pathlib import Path
from revolt_hostctl.app.models import Host, Network


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


def network_objects_generator(count):
    for i in range(count):
        name = f"{Network.__name__}{i}"
        cidr = f"10.0.0.0/{i}"
        yield Network(name=name, cidr=cidr)


def host_object_generator(count):
    for i in range(count):
        name = f"{Host.__name__}{i}"
        mac_address = f"00:00:00:00:00:h{i}"
        yield Host(name=name, mac_address=mac_address)


def assert_objs_equal(left, right, exclude=None) -> None:
    exclude = exclude or []
    for attr_name in left.__dict__.keys():
        if attr_name in exclude:
            continue
        assert getattr(left, attr_name) == getattr(right, attr_name)
