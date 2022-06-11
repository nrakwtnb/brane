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


# define the types for universal objects


def _generate_file_type():
    import io
    import pathlib

    PathType = Union[str, pathlib.Path]
    FileType = Union[PathType, io.TextIOWrapper]  # [TODO]: more types should be added
    return PathType, FileType


PathType, FileType = _generate_file_type()
del _generate_file_type


# define the package specific types


class ModuleClassType:
    _registered_subclasses: dict
    priority: int
    name: Optional[str]
    module: Any
    loaded: bool
    module_read_method: Optional[Callable]
    module_read_method_name: Optional[str]
    file_read_method_name: Optional[str]
    file_open_for_read: bool
    open_mode_for_read: dict[str, Any]
    transform: Optional[Callable]
    transform_name: Optional[str]
    transform_info: Optional[tuple[str, ...]]

    module_write_method: Callable = None
    module_write_method_name: Optional[str]
    writer_method_name: Optional[str]
    object_write_method_name: Optional[str]
    file_write_method_name: Optional[str]
    file_open_for_write: bool
    open_mode_for_write: dict[str, Any]

    file_arg_first: bool
    object_unpacking_type: str
    file_keyword_at_write: Optional[str]
    obj_keyword_at_write: Optional[str]

    base_args_read: tuple
    base_kwargs_read: dict
    base_args_write: tuple
    base_kwargs_write: dict
    # generate_params_read
    # generate_params_write


class FormatClassType:
    pass


class ObjectClassType:
    pass


class HookClassType:
    pass


class EventClassType:
    pass


HookFlagType = Optional[Union[str, set[str]]]


class ContextInterface(TypedDict):
    object: Optional[Any] = None
    objects: Optional[list[Any]] = None
    path: Optional[PathType] = None
    paths: Optional[list[PathType]] = None
    file: Optional[FileType] = None
    files: Optional[list[FileType]] = None
    Module: Optional[ModuleClassType] = None
    Format: Optional[FormatClassType] = None


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
