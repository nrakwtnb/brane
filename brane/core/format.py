from __future__ import annotations
from brane.typing import *
from brane.core.base import BaseSubclassRegister
from brane.core.base import MetaFalse
import importlib


def normalize_extension_default(ext: str) -> str:
    return ext.strip().lower()


class MetaFormat(type):
    def __new__(cls, classname, bases, class_info):
        new_class_info = class_info.copy()
        default_extension: Optional[str] = class_info.get("default_extension", None)
        if new_class_info.get("name", None) is None:
            new_class_info["name"] = default_extension
        if default_extension not in class_info.get("variation", []):
            new_class_info.setdefault("variation", []).append(default_extension)
        print(f"[DEBUG]: in MetaFormat default_extension={default_extension} class_info={new_class_info}")
        return type.__new__(cls, classname, bases, new_class_info)


class Format(FormatClassType, BaseSubclassRegister, metaclass=MetaFormat):
    # Image, Text ... # experimental
    data_type = None
    # jpg, png, tsv,... (flexible/variable/dynamical)
    default_extension: Optional[str] = None

    # valid = True
    
    #_registered_subclasses = []
    _registered_subclasses = {}#OrderedDict()
    registered_formats = _registered_subclasses
    # registered_formats = []
    # def __init_subclass__(cls):
    #     if cls.valid:
    #         cls.registered_formats.append(cls)
    #     # これだと継承クラス全体でregistered_moduleをシェア
    
    # valid for python >= 3.9
    # [TODO]: remove metaclass and use the follwoing lines if python < 3.9 are forbidden
    # @classmethod
    # @property
    # def name(cls):
    #     return cls.default_extension


    # integrated from Extension
    variation: list[str] = []# variations ? // use tuple instead of list or replace later ?

    @classmethod
    def check_extension(cls, ext: str):
        ext_normalized: str = normalize_extension_default(ext)
        return ext_normalized in cls.variation

class MetaNoneFormat(MetaFormat, MetaFalse):# [MEMO]: deprecated after removing MetaFormat
    pass

class NoneFormat(Format, metaclass=MetaNoneFormat):
    valid = False
