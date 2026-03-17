from pathlib import Path
from functools import wraps
from dataclasses import fields
from importlib.metadata import version, PackageNotFoundError
from revolt_hostctl.app.config import Config
from revolt_hostctl.app.logger import Logger
from revolt_hostctl.adapters.storage.shelve_db import ShelveAdapter
from revolt_hostctl.core.storage import Storage
from revolt_hostctl.core.utils import print_table


class App:
    def __init__(self, root_dir: Path):
        self.config = Config(root_dir)
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
    def add_obj(self, args):
        obj_type, args = self._parse_obj_type(args)
        params = self._parse_params(args)
        klass = self.storage.CLASS_MAP[obj_type]
        obj = klass(**params)
        stored_obj = self.storage.get(obj_type, obj.id)
        if stored_obj is not None:
            raise ValueError(f"Object {obj} already exists")
        return self.storage.add(obj)

    @with_logging
    @with_storage_transaction
    def get_obj(self, args):
        obj_type, args = self._parse_obj_type(args)
        params = self._parse_params(args)
        klass = self.storage.CLASS_MAP[obj_type]
        obj = klass(**params)
        stored_obj = self.storage.get(obj.storage_key, obj.id)
        print(stored_obj)

    @with_logging
    @with_storage_transaction
    def update_obj(self, args):
        obj_type, args = self._parse_obj_type(args)
        params = self._parse_params(args)
        klass = self.storage.CLASS_MAP[obj_type]
        obj = klass(**params)
        stored_obj = self.storage.get(obj_type, obj.id)
        if stored_obj is None:
            raise ValueError(f"Object {obj} does not exist")
        for field in fields(obj):
            if field.name == "created_at":
                continue
            attr = getattr(obj, field.name)
            if attr is None:
                continue
            setattr(stored_obj, field.name, attr)
        return self.storage.update(stored_obj)

    @with_logging
    @with_storage_transaction
    def remove_obj(self, args):
        obj_type, args = self._parse_obj_type(args)
        params = self._parse_params(args)
        klass = self.storage.CLASS_MAP[obj_type]
        obj = klass(**params)
        self.storage.remove(obj)

    @with_storage_transaction
    def list_objs(self, args):
        obj_type, _ = self._parse_obj_type(args)
        obj_list = self.storage.list(obj_type)

        print_table(obj_list)

    def help(self):
        print(
            "Usage: revolt-hostctl <command> [options]\n"
            "\n"
            "Commands:\n"
            "  -add <obj_type> <params>      Add a new <obj_type> object\n"
            "  -get <obj_type> <params>      Get an <obj_type> object by ID\n"
            "  -update <obj_type> <params>   Update an existing <obj_type> object\n"
            "  -remove <obj_type> <id=>      Remove an <obj_type> object by ID\n"
            "  -list <obj_type>              List all <obj_type> objects\n"
            "  -help, -h                     Show this help message\n"
            "  -version                      Show version information\n"
        )

    def version(self):
        try:
            print(version(self.config.app_name))
        except PackageNotFoundError:
            print("0.0.0+dev")

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
