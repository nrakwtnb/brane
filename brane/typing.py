from __future__ import annotations

from typing import (  # noqa: F401
    Any,
    Callable,
    Container,
    Generator,
    Generic,
    NamedTuple,
    Optional,
    Sequence,
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


# define the package specific types


class ModuleClassType:
    name: str
    loaded: bool
    load_modules: Callable
    reload_modules: Callable
    read: Callable
    write: Callable


class FormatClassType:
    module: ModuleClassType


class ObjectClassType:
    module: ModuleClassType
    format: FormatClassType
    object: Any


HookFlagType = Optional[Union[str, set[str]]]


class HookClassType(Callable):
    hook_name: Optional[str]
    flag: HookFlagType
    active: bool
    condition: Callable[ContextInterface, bool]


class EventClassType:
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
    if os.environ.get("BRANE_MODE", None) == 'debug':
        builtins.print(*value, end=end, file=file, flush=flush)
    else:
        pass
