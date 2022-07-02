from __future__ import annotations

from brane.core.base import BaseSubclassRegister, MetaFalse
from brane.typing import *  # noqa: F403


def normalize_extension_default(ext: str) -> str:
    return ext.strip().lower()


class MetaFormat(type):
    def __new__(cls, classname: str, bases: tuple[type], class_info: dict):
        new_class_info: dict = class_info.copy()
        default_extension: Optional[str] = class_info.get("default_extension", None)
        if new_class_info.get("name", None) is None:
            new_class_info["name"] = default_extension
        if default_extension not in class_info.get("variation", []):
            new_class_info.setdefault("variation", []).append(default_extension)

        print(f"[DEBUG]: in MetaFormat default_extension={default_extension} class_info={new_class_info}")
        return type.__new__(cls, classname, bases, new_class_info)

    # [TODO] python>=3.9, move to class as classmethod property
    @property
    def registered_formats(cls) -> dict[str, FormatClassType]:
        # [ARG]: It assumes it is used as mixin with BaseSubclassRegister.
        #     And this line raises mypy error ("MetaFormat" has no attribute "_registered_subclasses").
        # return cls._registered_subclasses
        return cls.get_registered_subclasses()


class Format(FormatClassType, BaseSubclassRegister, metaclass=MetaFormat):
    _registered_subclasses: dict[str, FormatClassType] = {}
    priority: int = 50
    module: Optional[ModuleClassType] = None
    # valid = True

    # # Image, Text ... # experimental
    # data_type = None
    # jpg, png, tsv,... (flexible/variable/dynamical)
    default_extension: Optional[str] = None
    variation: list[str] = []  # variations ? // use tuple instead of list or replace later ?

    @classmethod
    def check_extension(cls, ext: str) -> bool:
        ext_normalized: str = normalize_extension_default(ext)
        return ext_normalized in cls.variation


class FormatConfig:
    # [base]
    name: Optional[str] = None
    priority: int = 50

    module_name: Optional[str] = None
    default_extension: Optional[str] = None
    variation: list[str] = []  # variations ? // use tuple instead of list or replace later ?


class FormatTemplate(Format, FormatConfig):
    pass


class MetaNoneFormat(MetaFormat, MetaFalse):  # [MEMO]: deprecated after removing MetaFormat
    pass


class NoneFormat(FormatClassType, metaclass=MetaNoneFormat):
    valid = False
