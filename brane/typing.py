from __future__ import annotations
from typing import Any, Union, Optional, Callable, Sequence, Generator, Generic, Tuple, Dict, List, Set, NamedTuple, TypeVar
from typing_extensions import Protocol

try:
    from typing import TypedDict # >=3.8
except ImportError:
    from typing_extensions import TypedDict # <=3.7

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

class ContextInterface(TypedDict):
    object = None
    objects = None
    path = None
    paths = None
    file = None
    files = None
    Module = None


def _generate_file_type():
    import pathlib
    import io
    PathType = Union[str, pathlib.Path]
    FileType = Union[PathType, io.TextIOWrapper]# [TODO]: more types should be added
    return PathType, FileType

PathType, FileType = _generate_file_type()
del _generate_file_type
