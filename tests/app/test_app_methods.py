import pytest
import time

from tests.utils import try_func
from revolt_hostctl.app.app import App
from tests.utils import assert_objs_equal


@pytest.fixture
def arg_params():
    return {
        "network": ["network", "name=network1", "cidr=10.0.0.0/24"],
        "host": ["host", "name=host1", "mac_address=aa:bb:cc:dd:ee:ff"]
    }


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

def test_add_update_get_list_remove_methods(tmp_path, arg_params):
    app = App(tmp_path)

    for args in arg_params.values():
        obj = app.add_obj(args)

        args = [obj.storage_key, f"id={obj.id}"]
        stored_obj = app.get_obj(args)
        assert_objs_equal(obj, stored_obj)

        stored_obj.name = stored_obj.name + "_updated"

        args = [stored_obj.storage_key]
        for k, v in stored_obj.to_dict().items():
            if v is None:
                continue
            args.append(f"{k}={v}")

        time.sleep(1)
        updated_obj = app.update_obj(args)

        assert updated_obj.name == obj.name + "_updated"
        assert_objs_equal(updated_obj, stored_obj, ["name", "updated_at"])
        assert updated_obj.updated_at > stored_obj.updated_at

        args = [updated_obj.storage_key, f"id={updated_obj.id}"]
        app.remove_obj(args)
        resp = app.get_obj(args)

        assert resp is None
