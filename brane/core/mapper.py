from __future__ import annotations
from brane.typing import *
from brane.core.module import NoneModule
from brane.core.format import NoneFormat
from brane.core.object import Object
from brane.core.extension import Extension, NoneExtension

class Extension2Extension():### rename
    # [TODO];: caching
    @classmethod
    def get_extension_class(cls, ext: str) -> ExtensionClassType:# ignore: this type is defined later
        for _, Ext in Extension.registered_extensions.items():###
            ext_normalzied = Ext.preprocess(ext)
            if ext_normalzied in Ext.variation:
                return Ext
        assert False, "no extension found"# [TODO]: エラーをraiseするか、NoneExtensionをreturnするか
        return NoneExtension

class Extension2Format(Extension2Extension):
    #def get_format_from_extension_name(ext):
    @classmethod
    def get_format(cls, ext: str) -> FormatClassType:
        Ext = cls.get_extension_class(ext)
        if Ext:###
            return Ext.format
        else:
            return NoneFormat

class Extension2Module(Extension2Extension):
    @classmethod
    def get_module(cls, ext: str) -> ModuleClassType:
        Ext = cls.get_extension_class(ext)
        if Ext:
            if hasattr(Ext, "module"):
                return Ext.module
            else:
                Fmt = Ext.format
                if hasattr(Fmt, "module"):
                    return Fmt.module
                else:
                    raise NotImplementedError
        else:
            assert False, "no module found"# [TODO]: エラーをraiseするか、NoneModuleをreturnするか
            return NoneModule
# if fmt is given, it priotize
# if necesaryy, also return format (may be used to decide filename extention)

# In the future, I'd like to use hashed-key for quick search
class ObjectFormat2Module:
    def get_module_from_object(obj, fmt=None) -> ModuleClassType:
        for _, Obj in Object.registered_objects.items():### -> global var.
            # type(obj) == Obj.object # Objにtype-eq評価か、isinstance評価か決めるattributeを付与したので、そちらで制御
            Obj.load_objects()### will be removed in the future
            #     -> Objのattributes (objectなどload_objectsでセットされるもの)にアクセスした際に、自動で読み出されるようにするため
            if isinstance(obj, Obj.object):
                if hasattr(Obj, "module") and Obj.module is not None:
                    module = Obj.module
                    return module
                elif hasattr(Obj, "module_checker"):
                    if hasattr(Obj, "format") and Obj.format is not None:
                        fmt = Obj.format
                        print("Obj.format", fmt)
                    elif hasattr(Obj, "format_checker") and Obj.format_checker is not None:
                        fmt = Obj.format_checker(obj)
                        print("Obj.format_checker", fmt)
                    module = Obj.module_checker(obj, fmt)
                    print("module", module)
                    return module
        assert False, "no object found"# [TODO]: エラーをraiseするか、NoneModuleをreturnするか
        return NoneObject
