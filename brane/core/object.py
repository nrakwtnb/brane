from __future__ import annotations
from brane.typing import *
from brane.core.base import BaseSubclassRegister

class MetaObject(type):
    def __new__(cls, classname, bases, class_info):
        #print(f"[DEBUG]: @MetaObject, cls={cls}, classname={classname} bases={bases}, class_info={class_info}")
        class_info["name"] = classname#class_info.get("__name__", None)
        return type.__new__(cls, classname, bases, class_info)

    @property
    def object(cls):
        cls.load_objects()
        print("@Meta:", cls)
        return cls.object_type

class Object(ObjectClassType, BaseSubclassRegister, metaclass=MetaObject):
    # required
    format = None
    module = None
    # registered_objects が自身を含むため、仮で設定 (定義しておかないと、get_module_from_objectで、Object.objectにアクセスしようとして怒られてしまう)
    object_type = type### temporal
    
    # optional
    type_evaluation = None
    format_checker = None
    module_checker = None

    _registered_subclasses = {}#[]
    registered_objects = _registered_subclasses

    #  valid = True
    #  registered_objects = []
    #  def __init_subclass__(cls):
    #      if valid:
    #          cls.registered_objects.append(cls)
    
    @classmethod
    def load_objects(cls):
        pass
        #raise NotImplementedError
    
    #@property
    #def name(cls):
    #    return cls.__name__
    #    #return str(cls.module.object)
