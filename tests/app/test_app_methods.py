from tests.utils import try_func
from revolt_hostctl.app.app import App


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
