from __future__ import annotations
from brane.typing import *
from brane.core.module import NoneModule
from brane.core.format import Format, NoneFormat
from brane.core.object import Object

class ExtensionMapper():### rename
    # [TODO];: caching
    @classmethod
    def get_format_class_from_extension(cls, ext: str) -> FormatClassType:# ignore: this type is defined later
        for _, Fmt in Format.registered_formats.items():
            if Fmt.check_extension(ext):
                return Fmt
        assert False, "no Format found"# [TODO]: エラーをraiseするか、NoneExtensionをreturnするか
        return NoneFormat

    @classmethod
    def get_module_class_from_extension(cls, ext: str) -> ModuleClassType:
        Fmt: FormatClassType = cls.get_format_class_from_extension(ext=ext)
        if Fmt:
            if hasattr(Fmt, "module"):
                return Fmt.module
            else:
                raise AttributeError(f"'module' attribute is not defined at {Fmt}")
        else:
            assert False, "no module found"# [TODO]: エラーをraiseするか、NoneModuleをreturnするか
            return NoneModule
# if fmt is given, it priotize
# if necesaryy, also return format (may be used to decide filename extention)

# In the future, I'd like to use hashed-key for quick search
class ObjectFormat2Module:
    # [TODO]: use hash ?
    def get_module_from_object(obj, fmt=None) -> ModuleClassType:
        for _, Obj in Object.registered_objects.items():### -> global var.
            # type(obj) == Obj.object # Objにtype-eq評価か、isinstance評価か決めるattributeを付与したので、そちらで制御
            Obj.load_objects()### will be removed in the future
            #     -> Objのattributes (objectなどload_objectsでセットされるもの)にアクセスした際に、自動で読み出されるようにするため
            if isinstance(obj, Obj.object):
                if hasattr(Obj, "module") and Obj.module is not None:
                    module = Obj.module
                    return module
                elif hasattr(Obj, "module_checker") and Obj.module_checker is not None:
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
