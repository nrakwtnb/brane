from __future__ import annotations

from typing import (  # noqa: F401
    Any,
    Callable,
    Container,
    Final,
    Generator,
    Generic,
    NamedTuple,
    NewType,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)

try:
    from typing import Literal, Protocol, TypedDict  # noqa: F401 # >=3.8
except ImportError:
    from typing_extensions import Literal, Protocol, TypedDict  # noqa: F401 # <=3.7


# define the types for universal objects


def _generate_file_related_types():
    import io
    import pathlib

    class IO(Protocol):
        def open(file):
            pass

    from fsspec.asyn import AsyncFileSystem

    PathType = Union[str, pathlib.Path]
    FileType = Union[io._io._IOBase]  # [TODO]: more types should be added
    IOType = Union[IO, AsyncFileSystem]  # [TODO]: more types should be added
    return PathType, FileType, IOType


PathType, FileType, IOType = _generate_file_related_types()
del _generate_file_related_types


AnyObjectType = Any

# define the package specific types


class ModuleType:
    name: Optional[str]  # or str ?
    loaded: bool
    load_modules: Callable[[], None]
    reload_modules: Callable[[], None]
    read: Callable
    write: Callable


class FormatType:
    module: Optional[ModuleClassType]
    check_extension: Callable[[str], bool]


class ObjectType:
    module: Optional[ModuleClassType]
    format: Optional[FormatClassType]
    object: AnyObjectType
    load_objects: Callable[[], None]
    # [ARG]: optional ?
    format_checker: Optional[Callable[[AnyObjectType], FormatClassType]]
    module_checker: Optional[Callable[[AnyObjectType, FormatClassType], ModuleClassType]]


ModuleClassType = Type[ModuleType]
FormatClassType = Type[FormatType]
ObjectClassType = Type[ObjectType]

HookMarkerType = Optional[Union[str, set[str]]]


class HookType:
    hook_name: Optional[str]
    marker: HookMarkerType
    active: bool  # [FIX] error: Signature of "active" incompatible with supertype "HookClassType"
    activate: Callable
    deactivate: Callable
    condition: Callable[[ContextInterface], bool]
    __call__: Callable[[ContextInterface], Union[ContextInterface, None]]


HookClassType = Type[HookType]


class EventType:
    clear_hooks: Callable
    add_hooks: Callable
    remove_hooks: Callable


class ContextInterface(TypedDict, total=False):
    object: Optional[Any]
    objects: Union[None, Any, list[Any], dict[str, Any]]
    path: Optional[PathType]
    paths: Union[None, list[PathType], dict[str, PathType]]
    ext: Optional[str]
    protocol: Optional[str]
    file: Optional[FileType]
    files: Union[None, list[FileType], dict[str, FileType]]
    args: tuple
    kwargs: dict[str, Any]  # [ARG]: mutable -> immutable
    Module: Optional[ModuleClassType]
    Format: Optional[FormatClassType]


# used for debug purpose temporalily
def print(*value, sep=' ', end='\n', file=None, flush=False):
    import builtins
    import os
    import sys

    if file is None:
        file = sys.stdout
    if 'debug' in os.environ.get("BRANE_MODE", ""):
        builtins.print(*value, end=end, file=file, flush=flush)
    else:
        pass
