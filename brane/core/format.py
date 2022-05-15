from __future__ import annotations
from brane.typing import *
from brane.core.base import BaseSubclassRegister

class MetaFormat(type):
    def __new__(cls, classname, bases, class_info):
        class_info["name"] = class_info.get("default_extension", None)
        return type.__new__(cls, classname, bases, class_info)

#class Format():
class Format(FormatClassType, BaseSubclassRegister, metaclass=MetaFormat):
    # Image, Text ...
    data_type = None
    # jpg, png, tsv,... (flexible/variable/dynamical)
    default_extension = None
    ## experimental attr & name
    #module_read = None
    ## experimental attr & name
    #module_write = None
    #
    #def read(self, obj):
    #    raise NotImplementedError
    #
    #def write(self, obj):
    #    raise NotImplementedError
    
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
from brane.core.base import MetaFalse
class MetaNoneFormat(MetaFormat, MetaFalse):# [MEMO]: deprecated after removing MetaFormat
    pass

class NoneFormat(Format, metaclass=MetaNoneFormat):
    valid = False
