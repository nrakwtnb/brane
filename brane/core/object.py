from __future__ import annotations

import importlib

from brane.core.base import BaseSubclassRegister
from brane.typing import *  # noqa: F403


class MetaObject(type):
    def __new__(cls, classname, bases, class_info):
        # print(f"[DEBUG]: @MetaObject, cls={cls}, classname={classname} bases={bases}, class_info={class_info}")
        new_class_info = class_info.copy()
        new_class_info["name"] = classname  # class_info.get("__name__", None)
        return type.__new__(cls, classname, bases, new_class_info)

    @property
    def object(cls):
        cls.load_objects()
        print("@Meta:", cls)
        return cls.object_type

    @property
    def registered_objects(cls):
        return cls._registered_subclasses


class Object(ObjectClassType, BaseSubclassRegister, metaclass=MetaObject):
    _registered_subclasses = {}
    priority = 50

    # required
    format = None
    module = None
    # registered_objects が自身を含むため、仮で設定 (定義しておかないと、get_module_from_objectで、Object.objectにアクセスしようとして怒られてしまう)
    object_type = type  ### temporal
    object_type_info = None  ### temporal

    # optional
    type_evaluation = None
    format_checker = None
    module_checker = None

    @classmethod
    def load_objects(cls):
        if cls.object_type_info:
            module_name, *obj_attr = cls.object_type_info
            module = importlib.import_module(module_name)
            obj = module
            for attr in obj_attr:
                obj = getattr(obj, attr)
            cls.object_type = obj
