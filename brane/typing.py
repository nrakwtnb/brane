from __future__ import annotations

from typing import (  # noqa: F401
    Any,
    Callable,
    Dict,
    Generator,
    Generic,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypeVar,
    Union,
)

try:
    from typing import Protocol, TypedDict  # noqa: F401 # >=3.8
except ImportError:
    from typing_extensions import Protocol, TypedDict  # noqa: F401 # <=3.7


class ModuleClassType:
    pass


class FormatClassType:
    pass


class ObjectClassType:
    pass


class HookClassType:
    pass


class EventClassType:
    pass


def _generate_file_type():
    import io
    import pathlib

    PathType = Union[str, pathlib.Path]
    FileType = Union[PathType, io.TextIOWrapper]  # [TODO]: more types should be added
    return PathType, FileType


PathType, FileType = _generate_file_type()
del _generate_file_type


class ContextInterface(TypedDict):
    object: Optional[Any] = None
    objects: Optional[list[Any]] = None
    path: Optional[PathType] = None
    paths: Optional[list[PathType]] = None
    file: Optional[FileType] = None
    files: Optional[list[FileType]] = None
    Module: Optional[ModuleClassType] = None
    Format: Optional[FormatClassType] = None
