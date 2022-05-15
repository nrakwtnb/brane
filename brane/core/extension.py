from __future__ import annotations
from brane.typing import *
from brane.core.format import Format
# class-dependency: Format

class NormalExtension2Format:
    ext2format = { format.default_extension: format for _, format in Format.registered_formats.items() }

    @classmethod
    def get_format_from_normalized_extension(cls, ext_name):
        # dynamically generated
        ext2format_dyn = { format.default_extension: format for _, format in Format.registered_formats.items() }
        return ext2format_dyn.get(ext_name, None)
# class-dependency: Extension2Format

class MetaExtension(type):
    def __new__(cls, classname, bases, class_info):
        new_class_info = class_info.copy()
        ext_name = class_info.get("name", None)# [TODO]: name keyを必ずもつ必要が有るか？
        #fmt = Extension2Format.ext2format.get(ext_name, None)# [TODO]: refine in the future
        #fmt = Extension2Format.get_format(ext_name)# [TODO]: refine in the future
        #fmt = NormalExtension2Format.ext2format.get(ext_name, None)# [TODO]: refine in the future
        fmt = NormalExtension2Format.get_format_from_normalized_extension(ext_name)# [TODO]: refine in the future
        print(f"[DEBUG]: in MetaExtension ext_name={ext_name} fmt={fmt} class_info={class_info}")
        if fmt:
            new_class_info.update({"format": fmt})
        if ext_name not in class_info.get("variation", []):
            new_class_info.setdefault("variation", []).append(ext_name)
        return type.__new__(cls, classname, bases, new_class_info)
from brane.core.base import BaseSubclassRegister

def normalize_extension_default(ext):
    return ext.strip().lower()

class Extension(ExtensionClassType, BaseSubclassRegister, metaclass=MetaExtension):
    #__metaclass__ = metaExtension # seem not to work (use meclass in class definition)
    name = None
    format = None
    
    # registered_objects が自身を含むため、仮で設定 (定義しておかないと、get_module_from_objectで、Object.objectにアクセスしようとして怒られてしまう)
    # 本来はNoneで設定していた
    variation = []# variations ? // use tuple instead of list or replace later ?
    
    preprocess = normalize_extension_default
    
    _registered_subclasses = {}#[]
    registered_extensions = _registered_subclasses

    # registered_formats = []
    # def __init_subclass__(cls):
    #     cls.registered_formats.append(cls)
    #     # これだと継承クラス全体でregistered_moduleをシェア
from brane.core.base import MetaFalse

class MetaNoneExtension(MetaExtension, MetaFalse):
    pass

class NoneExtension(Extension, metaclass=MetaNoneExtension):
    valid = False
