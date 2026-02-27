from pathlib import Path
from functools import wraps
from dataclasses import fields
from importlib.metadata import version, PackageNotFoundError
from revolt_hostctl.app.config import Config
from revolt_hostctl.app.logger import Logger
from revolt_hostctl.adapters.storage.shelve_db import ShelveAdapter
from revolt_hostctl.core.storage import Storage


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
            raise Exception(f"Object {obj} already exists")
        self.storage.add(obj)

    @with_logging
    @with_storage_transaction
    def update_obj(self, args):
        obj_type, args = self._parse_obj_type(args)
        params = self._parse_params(args)
        klass = self.storage.CLASS_MAP[obj_type]
        obj = klass(**params)
        stored_obj = self.storage.get(obj_type, obj.id)
        if stored_obj is None:
            raise Exception(f"Object {obj} does not exist")
        for field in fields(obj):
            attr = getattr(obj, field.name)
            if attr is None:
                continue
            setattr(stored_obj, field.name, attr)
        self.storage.update(stored_obj)

    @with_logging
    @with_storage_transaction
    def remove_obj(self, args):
        obj_type, args = self._parse_obj_type(args)
        params = self._parse_params(args)
        klass = self.storage.CLASS_MAP[obj_type]
        obj = klass(**params)
        self.storage.remove(obj)

    def list_objs(self, args):
        obj_type, _ = self._parse_obj_type(args)
        obj_list = self.storage.list(obj_type)
        for obj in obj_list:
            print(obj)

    def help(self):
        pass

    def version(self):
        try:
            print(version(self.config.app_name))
        except PackageNotFoundError:
            print("0.0.0+dev")

    def _parse_obj_type(self, args: list, no_raise: bool = False) -> tuple:
        obj_type = args.pop(0) if len(args) else None
        if not no_raise and obj_type is None:
            raise Exception("No obj type provided")
        if obj_type not in self.storage.COLLECTIONS:
            raise Exception(f"Invalid obj type: {obj_type}")
        return obj_type, args

    def _parse_params(self, args: list) -> dict:
        params = dict()
        for i in args:
            i = i.strip()
            if "=" not in i:
                raise Exception(f"Invalid param: {i}")
            else:
                key, value = i.split("=")
                params[key] = value
        return params
