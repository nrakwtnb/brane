from __future__ import annotations
from brane.typing import *
from collections import OrderedDict

class BaseSubclassRegister():
    valid = True
    #_registered_subclasses = []
    # __registered_subclasses = []# cls.__registered_subclasses でアクセスできない# [ToDo]
    _registered_subclasses = OrderedDict()
    
    priority: int = -1

    def __init_subclass__(cls):
        # [idea memo]: nameがNoneの時は登録しないとか
        if cls.valid:
            #cls._registered_subclasses.append(cls)
            name = getattr(cls, "name", None)
            if name in cls._registered_subclasses:# for debug
                print(f"[DEBUG]: overwritten cls.name = {name}, cls = {cls}")
            else:
                print(f"[DEBUG]: register cls.name = {name}, cls = {cls}")
            cls._registered_subclasses.update({ name : cls })
        # これだと継承クラス全体でregistered_moduleをシェア


class MetaFalse(type):
    def __new__(cls, classname, bases, class_info):
        new_class_info = class_info.copy()
        new_class_info.update({"__bool__": lambda cls:False})
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
