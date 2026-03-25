# tests/test_models.py

import uuid
import pytest

from revolt_hostctl.core.models import BaseModel, Host, Network


def test_basemodel_generates_default_fields():
    obj = BaseModel()

    assert isinstance(obj.id, str)
    assert obj.id != ""

    assert isinstance(obj.created_at, int)
    assert isinstance(obj.updated_at, int)


def test_storage_key_uses_class_name():
    assert BaseModel().storage_key == "basemodel"
    assert Host().storage_key == "host"
    assert Network().storage_key == "network"


def test_to_dict_returns_model_fields_only():
    obj = Host(
        id="h1",
        created_at=100,
        updated_at=200,
        name="host1",
        mac_address="aa:bb:cc:dd:ee:ff",
        ip_addresses={"10.0.0.1"},
        os="linux",
        os_version="ubuntu",
        description="test host",
    )

    data = obj.to_dict()

    assert data == {
        "id": "h1",
        "created_at": 100,
        "updated_at": 200,
        "name": "host1",
        "mac_address": "aa:bb:cc:dd:ee:ff",
        "ip_addresses": {"10.0.0.1"},
        "os": "linux",
        "os_version": "ubuntu",
        "description": "test host",
    }


def test_ordered_items_puts_id_first_and_timestamps_last():
    obj = Network(
        id="n1",
        created_at=100,
        updated_at=200,
        name="net1",
        cidr="192.168.1.0/24",
    )

    items = obj._ordered_items()
    keys = [k for k, _ in items]

    assert keys[0] == "id"
    assert keys[-2] == "created_at"
    assert keys[-1] == "updated_at"

    assert "name" in keys
    assert "cidr" in keys


def test_get_table_row_returns_values_in_requested_order():
    obj = Host(
        id="h1",
        created_at=1700000000,
        updated_at=1700000100,
        name="host1",
        mac_address="aa:bb:cc:dd:ee:ff",
    )

    row = obj.get_table_row(["id", "name", "mac_address"])

    assert row == ["h1", "host1", "aa:bb:cc:dd:ee:ff"]


def test_get_table_row_formats_timestamp_fields():
    obj = BaseModel(
        id="x1",
        created_at=1700000000,
        updated_at=1700000100,
    )

    row = obj.get_table_row(["created_at", "updated_at"])

    assert isinstance(row[0], str)
    assert isinstance(row[1], str)
    assert row[0] != ""
    assert row[1] != ""

    # Не проверяем точную дату, чтобы тест не зависел от timezone окружения.
    assert len(row[0]) == 19
    assert len(row[1]) == 19


def test_get_table_row_returns_unknown_for_missing_field():
    obj = Host(name="host1")

    row = obj.get_table_row(["name", "invalid_field"])

    assert row == ["host1", "Unknown"]


def test_repr_contains_class_name_and_fields():
    obj = Network(
        id="n1",
        created_at=100,
        updated_at=200,
        name="net1",
        cidr="10.0.0.0/24",
    )

    value = repr(obj)

    assert "Network(" in value
    assert "id='n1'" in value
    assert "name='net1'" in value
    assert "cidr='10.0.0.0/24'" in value


def test_str_formats_none_as_dash_and_preserves_order():
    obj = Host(
        id="h1",
        created_at=100,
        updated_at=200,
        name="host1",
        mac_address=None,
        ip_addresses=None,
        os=None,
        os_version=None,
        description=None,
    )

    value = str(obj)
    lines = value.splitlines()

    assert lines[0].startswith("id")
    assert "h1" in lines[0]

    assert any(line.startswith("name") and "host1" in line for line in lines)
    assert any(line.startswith("mac_address") and "-" in line for line in lines)
    assert any(line.startswith("description") and "-" in line for line in lines)

    assert lines[-2].startswith("created_at")
    assert lines[-1].startswith("updated_at")


def test_custom_values_can_be_passed_explicitly():
    obj = BaseModel(
        id="fixed-id",
        created_at=111,
        updated_at=222,
    )

    assert obj.id == "fixed-id"
    assert obj.created_at == 111
    assert obj.updated_at == 222