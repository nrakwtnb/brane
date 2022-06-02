from __future__ import annotations

import importlib

from brane.core.base import BaseSubclassRegister, MetaFalse
from brane.core.utils import integrate_args, integrate_kwargs
from brane.typing import *  # noqa: F403


class MetaModule(type):
    def __new__(cls, classname, bases, class_info):
        new_class_info = class_info.copy()
        if new_class_info.get("name", None) is None:
            new_class_info["name"] = new_class_info.get("module_name", None)
        print(f"[DEBUG]: in MetaModule class_info={new_class_info}")
        return type.__new__(cls, classname, bases, new_class_info)

    @property
    def registered_modules(cls):
        return cls._registered_subclasses


class Module(ModuleClassType, BaseSubclassRegister, metaclass=MetaModule):
    """
    Needed to be inheritated. The child class correspond to module.
    """

    _registered_subclasses = {}
    priority = 50

    # should be unqiue. package name specifed at pip install is usually set
    name: Optional[str] = None
    # module name for base. allow the string like "module1.module2"
    module_name: Optional[str] = None
    # the module specified by the module_name is set at load_modules method
    module: Any = None
    # temporal / experimental
    loaded: bool = False

    module_method_read: Optional[str] = None
    read_method: Optional[Callable] = None

    module_method_write: Optional[str] = None
    write_method: Callable = None
    file_arg_first: bool = True

    file_open_for_read: bool = False
    open_mode_for_read: dict = {"mode": "r"}
    file_open_for_write: bool = False
    open_mode_for_write: dict = {"mode": "w"}

    object_method_write: Optional[str] = None  ### temporal arg name

    # temporal arg name # unnecessary ?
    # require_file_stream_read = False

    base_args_read: tuple = ()
    base_kwargs_read: dict = {}
    base_args_write: tuple = ()
    base_kwargs_write: dict = {}
    generate_params_read = None  # unnecessary ?
    generate_params_write = None

    @classmethod
    def load_modules(cls):
        """lazy loading of modules and setting of methods."""
        # allow lazy loading of modules
        if cls.module_name:
            if cls.module is None:
                cls.module = importlib.import_module(cls.module_name)
        # set read method
        if cls.module_method_read:
            cls.read_method = getattr(cls.module, cls.module_method_read)
        else:
            raise ValueError(
                "'module_method_read' is undefined"
            )  # [ARGS]: other error type ?
        # set write method
        if cls.module_method_write:
            cls.write_method = getattr(cls.module, cls.module_method_write)
        elif cls.object_method_write:
            pass
        else:
            raise ValueError(
                "neither 'module_method_write' nor 'object_method_write' is undefined"
            )  # [ARGS]: other error type ?

    @classmethod
    def read(
        cls,
        path: Optional[PathType] = None,
        file: Optional[FileType] = None,
        *args,
        **kwargs,
    ) -> Any:
        """read from path or file stream.

        Args:
            path: path object
            file: file stream object

        Returns:
            Any: loaded objects
        """
        # generate the args and keyword args passed to read method
        base_args_read, base_kwargs_read = (
            cls.base_args_read,
            cls.base_kwargs_read.copy(),
        )
        # [ARG]: unnecessary
        # if cls.generate_params_read:
        #     base_args_read, base_kwargs_read = cls.generate_params_read(base_args_read, base_kwargs_read)

        args_read = integrate_args(base_args_read, args)
        kwargs_read = integrate_kwargs(base_kwargs_read, kwargs)
        # ToDo: args and kwargs -> ???

        if file is None:
            if cls.file_open_for_read:
                file = open(path, **cls.open_mode_for_read)
            else:
                file = path

        if cls.read_method:
            obj = cls.read_method(file, *args_read, **kwargs_read)
            return obj
        else:
            raise NotImplementedError

        if cls.file_open_for_read:
            file.close()

    @classmethod
    def write(
        cls,
        obj: Any,
        path: Optional[PathType] = None,
        file: Optional[FileType] = None,
        *args,
        **kwargs,
    ):
        """write objects to the file specified by path object or file object.

        Args:
            obj: object to save
            path: path object
            file: file stream object
        """
        base_args_write, base_kwargs_write = (
            cls.base_args_write,
            cls.base_kwargs_write.copy(),
        )
        if cls.generate_params_write:
            base_args_write, base_kwargs_write = cls.generate_params_write(
                obj, base_args_write, base_kwargs_write
            )

        args_write = integrate_args(base_args_write, args)
        kwargs_write = integrate_kwargs(base_kwargs_write, kwargs)

        if file is None:
            if cls.file_open_for_write:
                file = open(path, **cls.open_mode_for_write)
            else:
                file = path

        if cls.module_method_write:
            if cls.file_arg_first:
                cls.write_method(file, obj, *args_write, **kwargs_write)
            else:
                cls.write_method(obj, file, *args_write, **kwargs_write)
        elif cls.object_method_write and hasattr(obj, cls.object_method_write):
            getattr(obj, cls.object_method_write)(file, *args_write, **kwargs_write)
        else:
            raise NotImplementedError

        if cls.file_open_for_write:
            file.close()


class MetaNoneModule(
    MetaModule, MetaFalse
):  # [MEMO]: deprecated after removing MetaModule
    pass


class NoneModule(Module, metaclass=MetaNoneModule):
    valid = False  ###
    name = "None"

    # @classmethod # not work for class
    # def __bool__(cls):
    #    return False
