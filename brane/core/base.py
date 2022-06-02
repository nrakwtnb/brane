from __future__ import annotations

from collections import OrderedDict  # deprecated ? (builtin dict is already ordered)

from brane.core.utils import sort_mapper
from brane.typing import *  # noqa: F403


class BaseSubclassRegister(object):
    valid = True
    # __registered_subclasses = []# cls.__registered_subclasses でアクセスできない# [ToDo]
    _registered_subclasses = OrderedDict()  # not list
    priority: int = -1

    def __init_subclass__(cls):
        # [idea memo]: nameがNoneの時は登録しないとか
        if cls.valid:
            # cls._registered_subclasses.append(cls)
            name = getattr(cls, "name", None)
            if name in cls._registered_subclasses:  # for debug
                print(f"[DEBUG]: overwritten cls.name = {name}, cls = {cls}")
            else:
                print(f"[DEBUG]: register cls.name = {name}, cls = {cls}")
            # assume the base is one of Module, Format, Object
            base = cls.__base__
            if issubclass(base, BaseSubclassRegister) and base != BaseSubclassRegister:
                print(f"[DEBUG]: registered @ {base}")
                base._registered_subclasses.update({name: cls})
                # sort by priority
                base._registered_subclasses = OrderedDict(
                    sort_mapper(mapper=cls._registered_subclasses, key="priority")
                )
        # これだと継承クラス全体でregistered_moduleをシェア


class MetaFalse(type):
    def __new__(cls, classname: str, bases, class_info):
        new_class_info = class_info.copy()
        new_class_info.update({"__bool__": lambda cls: False})
        return type.__new__(cls, classname, bases, new_class_info)

    def __bool__(cls):
        return False


class Context(ContextInterface):
    """The context/state infomation in the IO flows.

    Attributes:
        object
        objects
        path
        paths
        file
        files
        Module

    """

    object = None
    objects = None
    path = None
    paths = None
    file = None
    files = None
    Module = None
