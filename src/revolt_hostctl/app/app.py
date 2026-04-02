import re
from pathlib import Path
from functools import wraps
from dataclasses import fields
from importlib.metadata import version, PackageNotFoundError
from revolt_hostctl.app.config import Config
from revolt_hostctl.app.logger import Logger
from revolt_hostctl.app.storage import Storage
from revolt_hostctl.app.utils import print_table
from revolt_hostctl.adapters.storage.shelve_db import ShelveAdapter


class App:
    def __init__(self):
        self.config = Config()
        self.logger = Logger(self.config)
        self.adapter = ShelveAdapter(self.config.storage_dir)
        self.storage = Storage(self.adapter)

    @staticmethod
    def with_storage_transaction(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.storage.load_state()
            try:
                result = func(self, *args, **kwargs)
            except Exception:
                raise
            self.storage.save_state()
            return result
        return wrapper

    @staticmethod
    def with_logging(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.logger.info(f"Running {func.__name__}")
            try:
                result = func(self, *args, **kwargs)
            except Exception as e:
                self.logger.error(f"Error: {e}")
                raise
            return result
        return wrapper

    @with_logging
    @with_storage_transaction
    def add_cmd(self, args):
        obj_type, params = self._get_type_and_params(args)
        obj = self.storage.CLASS_MAP[obj_type](**params)
        if self.storage.get(obj_type, obj.id):
            raise ValueError(f"Object {obj} already exists")
        return self.storage.add(obj)

    @with_logging
    @with_storage_transaction
    def get_cmd(self, args):
        obj_type, params = self._get_type_and_params(args)
        print(self._get_stored_obj(obj_type, params))

    @with_logging
    @with_storage_transaction
    def update_cmd(self, args):
        obj_type, params = self._get_type_and_params(args)
        stored_obj = self._get_stored_obj(obj_type, params)

        if stored_obj is None:
            raise ValueError(f"Object does not exist")

        for field in fields(stored_obj):
            if field.name in ["id", "created_at"]:
                continue
            if (attr := params.get(field.name)) is not None:
                setattr(stored_obj, field.name, attr)

        return self.storage.update(stored_obj)

    @with_logging
    @with_storage_transaction
    def remove_cmd(self, args):
        obj_type, params = self._get_type_and_params(args)
        if obj := self._get_stored_obj(obj_type, params):
            self.storage.remove(obj)

    @with_logging
    @with_storage_transaction
    def list_cmd(self, args):
        obj_type, _ = self._parse_obj_type(args)
        if not (obj_list := self.storage.list(obj_type)):
            return print("No objects found")

        headers = ["id", "name"]
        print_table([i.get_table_row(headers) for i in obj_list], headers)

    @with_logging
    @with_storage_transaction
    def clean_cmd(self):
        self.storage.clean_all()

    @with_logging
    @with_storage_transaction
    def parse_cmd(self, args):
        try:
            if not args:
                raise Exception("No path provided")

            path = Path(args[0])

            if not path.exists():
                raise Exception(f"File {path} does not exist")

            vm_dirs = [d for d in path.iterdir() if d.is_dir()]
            vm_paths = [d / f"{d.name}.vmx" for d in vm_dirs]

            data = {}

            for p in vm_paths:
                if not p.is_file():
                    continue
                lines = p.read_text()
                mac_match = re.search(
                    r'ethernet0\.address\s*=\s*"([0-9A-Fa-f:]{17})"',
                    lines
                )
                if not mac_match:
                    continue
                data[p] = mac_match.group(1)

            for k, v in data.items():
                print(f"{k}: {v}")

        except Exception as e:
            print(f"Error: {e}")
            exit(1)

    @with_logging
    @with_storage_transaction
    def version_cmd(self):
        try:
            print(version(self.config.app_name))
        except PackageNotFoundError:
            print("0.0.0+dev")

    def _get_type_and_params(self, args: list) -> tuple:
        obj_type, args = self._parse_obj_type(args)
        return obj_type, self._parse_params(args)

    def _get_stored_obj(self, obj_type: str, params: dict):
        if obj_id := params.get("id"):
            return self.storage.get(obj_type, obj_id)
        return self.storage.get(obj_type, self.storage.CLASS_MAP[obj_type](**params).id)

    def _parse_obj_type(self, args: list, pass_none: bool = False) -> tuple:
        resp_args = args[:]
        obj_type = resp_args.pop(0) if len(resp_args) else None

        if not pass_none and obj_type is None:
            raise ValueError("No obj type provided")

        if obj_type is not None and obj_type not in self.storage.COLLECTIONS:
            raise ValueError(f"Invalid obj type: {obj_type}")

        return obj_type, resp_args

    def _parse_params(self, args: list, silence: bool = False) -> dict:
        params = dict()
        for i in args:
            i = i.strip()
            if "=" not in i:
                if silence:
                    continue
                else:
                    raise ValueError(f"Invalid param: {i}")
            else:
                key, value = i.split("=")
                params[key] = value

        if not silence and not len(params.keys()):
            raise ValueError("No any params provided")

        return params
