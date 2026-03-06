import pytest

from tests.utils import try_func
from revolt_hostctl.app.app import App
from revolt_hostctl.core.models import Network, Host
from tests.utils import network_objects_generator, host_object_generator


def test_parse_obj_type(tmp_path):
    app = App(tmp_path)

    res, err = try_func(app._parse_obj_type, [])
    assert res is None
    assert isinstance(err, ValueError)

    res, err = try_func(app._parse_obj_type, [], True)
    assert isinstance(res, tuple)
    assert len(res) == 2
    assert res[0] is None
    assert isinstance(res[1], list) and len(res[1]) == 0
    assert err is None

    res, err = try_func(app._parse_obj_type, ["invalid"])
    assert res is None
    assert isinstance(err, ValueError)

    res, err = try_func(app._parse_obj_type, ["invalid", True])
    assert res is None
    assert isinstance(err, ValueError)

    for t in app.storage.COLLECTIONS:
        res, err = try_func(app._parse_obj_type, [t])
        assert isinstance(res, tuple)
        assert len(res) == 2
        assert res[0] == t
        assert err is None

        res, err = try_func(app._parse_obj_type, [t], True)
        assert isinstance(res, tuple)
        assert len(res) == 2
        assert res[0] == t
        assert err is None


def test_parse_params(tmp_path):
    app = App(tmp_path)

    params = ["param1=1", "param2=2", "param3=3"]
    res = app._parse_params(params)
    assert isinstance(res, dict)
    assert len(res.keys()) == 3
    assert res["param1"] == "1"
    assert res["param2"] == "2"
    assert res["param3"] == "3"

    params = ["param1=1", "param2=2", "param3"]
    res, err = try_func(app._parse_params, params)
    assert res is None
    assert isinstance(err, ValueError)

    res = app._parse_params(params, True)
    assert isinstance(res, dict)
    assert len(res.keys()) == 2
    assert res["param1"] == "1"
    assert res["param2"] == "2"

    params = []
    res, err = try_func(app._parse_params, params)
    assert res is None
    assert isinstance(err, ValueError)

    res = app._parse_params([], True)
    assert isinstance(res, dict)
    assert len(res.keys()) == 0


def test_crud_obj(tmp_path):
    app = App(tmp_path)

    items = {
        "network": {
            "name": "network1",
            "cidr": "192.168.1.0/24"
        },
        "host": {
            "name": "host1",
            "mac_address": "aa:bb:cc:dd:ee:ff"
        }
    }

    for t, props in items.items():
        args = [f"{k}={v}" for k, v in props.items()]
        args = [t] + args
        add_obj = app.add_obj(args)

        assert isinstance(add_obj, app.storage.CLASS_MAP[t])

        for k, v in items[t].items():
            assert v == getattr(add_obj, k)

        args = [t, f"id={add_obj.id}"]
        get_obj = app.get_obj(args)

        assert type(add_obj) is type(get_obj)
        assert add_obj.id == get_obj.id

        for k, v in add_obj.__dict__.items():
            assert v == getattr(get_obj, k)

        add_obj.name = add_obj.name + "_modified"
        args = [t, f"id={add_obj.id}", f"name={add_obj.name}"]
        app.update_obj(args)

        args = [t, f"id={add_obj.id}"]
        get_obj = app.get_obj(args)

        assert type(add_obj) is type(get_obj)
        assert add_obj.id == get_obj.id

        for k, v in add_obj.__dict__.items():
            if k == "updated_at":
                continue
            assert v == getattr(get_obj, k)

        args = [t, f"id={add_obj.id}"]
        app.remove_obj(args)

        args = [t, f"id={add_obj.id}"]
        get_obj = app.get_obj(args)

        assert get_obj is None
