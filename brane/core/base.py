from __future__ import annotations

from brane.core.utils import sort_mapper
from brane.typing import *  # noqa: F403


class BaseSubclassRegister(object):
    valid: bool = True
    # [CHECK]: cannot access to it by `cls.__registered_subclasses`
    _registered_subclasses: dict[str, type] = dict()
    priority: int = -1

    def __init_subclass__(cls):
        # [ARG]: not register the subclass if name is None ?
        if cls.valid:
            name = getattr(cls, "name", None)
            if name:
                if name in cls._registered_subclasses:  # inserted for debug purpose
                    print(f"[DEBUG]: overwritten cls.name = {name}, cls = {cls}")
                else:
                    print(f"[DEBUG]: register cls.name = {name}, cls = {cls}")
                # assume the base is one of Module, Format, Object
                base = cls.__base__
                if issubclass(base, BaseSubclassRegister) and base != BaseSubclassRegister:
                    print(f"[DEBUG]: registered @ {base}")
                    base._registered_subclasses.update({name: cls})

    @classmethod
    def get_registered_subclasses(cls) -> dict[str, type]:
        # sort by priority
        return sort_mapper(mapper=cls._registered_subclasses, key="priority")


class MetaFalse(type):
    def __new__(cls, classname: str, bases: tuple[type], class_info: dict):
        new_class_info = class_info.copy()
        new_class_info.update({"__bool__": lambda cls: False})
        return type.__new__(cls, classname, bases, new_class_info)

    def __bool__(cls) -> bool:
        return False


class Context(ContextInterface):
    """The context/state infomation in the IO flows.

    Attributes:
        object
        objects
        path
        paths
        protocol
        file
        files
        args
        kwargs
        Module
        Format

    """

    object: Optional[Any] = None
    objects: Union[None, Any, list[Any], dict[str, Any]] = None
    path: Optional[PathType] = None
    paths: Union[None, list[PathType], dict[str, PathType]] = None
    protocol: Optional[str] = None
    file: Optional[FileType] = None
    files: Union[None, list[FileType], dict[str, FileType]] = None
    args: tuple = ()
    kwargs: dict[str, Any] = {}  # [ARG]: mutable -> immutable
    Module: Optional[ModuleClassType] = None
    Format: Optional[FormatClassType] = None
