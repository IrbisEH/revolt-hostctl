import pytest

from tests.utils import try_func
from revolt_hostctl.app.app import App
from revolt_hostctl.core.models import Network, Host
from tests.utils import network_objects_generator, host_object_generator


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

    res = app._parse_params([])
    assert isinstance(res, dict)
    assert len(res.keys()) == 0


# def test_add_obj(tmp_path, arg_params):
#     # TODO: fix it! It mast testsing all params include ip_addresses lists
#     app = App(tmp_path)
#
#     for _type, args in arg_params.items():
#         obj = app.add_obj(args)
#
#         resp = app.get_obj(obj.storage_key, obj.id)
#
#         obj_type_name = obj.__class__.__name__
#         resp_type_name = resp.__class__.__name__
#
#         assert resp is not None
#         assert resp_type_name == obj_type_name
#
#         for prop_name in obj.__dict__.keys():
#             obj_attr = getattr(obj, prop_name)
#             resp_attr = getattr(resp, prop_name)
#             assert obj_attr == resp_attr
#
#         params = resp.to_dict()
#         params["name"] = params["name"] + "_modified"
#         args = [f"{k}={v}" for k, v in params.items() if isinstance(v, str)]
#         args = [_type] + args
#
#         app.update_obj(args)
#         resp = app.get_obj(obj.storage_key, obj.id)
#         resp_type_name = resp.__class__.__name__
#
#         assert resp is not None
#         assert resp_type_name == obj_type_name
#
#         for prop_name in resp.__dict__.keys():
#             modified_attr = params.get(prop_name)
#             resp_attr = getattr(resp, prop_name)
#             assert modified_attr == resp_attr
