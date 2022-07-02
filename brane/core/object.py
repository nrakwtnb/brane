from __future__ import annotations

import importlib

from brane.core.base import BaseSubclassRegister
from brane.typing import *  # noqa: F403


class MetaObject(type):
    def __new__(cls, classname: str, bases, class_info: dict[str, Any]):
        # print(f"[DEBUG]: @MetaObject, cls={cls}, classname={classname} bases={bases}, class_info={class_info}")
        new_class_info = class_info.copy()
        if "name" not in class_info:
            new_class_info["name"] = classname  # class_info.get("__name__", None)
        return type.__new__(cls, classname, bases, new_class_info)

    # [TODO] python>=3.9, move to class as classmethod property
    @property
    def object(cls) -> Any:
        cls.load_objects()
        print("@Meta:", cls)
        return cls.object_type

    # [TODO] python>=3.9, move to class as classmethod property
    @property
    def registered_objects(cls) -> dict[str, ObjectClassType]:
        # return cls._registered_subclasses
        return cls.get_registered_subclasses()


class Object(ObjectClassType, BaseSubclassRegister, metaclass=MetaObject):
    _registered_subclasses: dict[str, ObjectClassType] = {}
    name: Optional[str] = None
    priority: int = 50
    loaded: bool = False

    format: Optional[FormatClassType] = None  # required
    module: Optional[ModuleClassType] = None  # required
    object_type = None  ### [ARG]] should change the attribute name ?
    object_type_info: Optional[tuple[str, ...]] = None  ### [TODO]: change the attribute name

    # optional
    type_evaluation = None
    format_checker = None
    module_checker = None

    @classmethod
    def load_objects(cls):
        if cls.loaded:
            return None

        if cls.object_type:
            cls.loaded = True
            return None

        if getattr(cls, "object_type_info", None):
            module_name, *obj_attr = cls.object_type_info
            module = importlib.import_module(module_name)
            obj = module
            for attr in obj_attr:
                obj = getattr(obj, attr)
            cls.object_type = obj
        else:
            raise AssertionError

        cls.loaded = True


class ObjectConfig:
    format_name: Optional[str] = None
    module_name: Optional[str] = None
    object_type_info: Optional[tuple[str, ...]] = None
    priority: int = 50


class ObjectTemplate(Object, ObjectConfig):
    name: Optional[str] = None
    object_type = None  ### [ARG]] should change the attribute name ?
    object_type_info: Optional[tuple[str, ...]] = None  ### [TODO]: change the attribute name
