from __future__ import annotations
from brane.typing import *
from brane.core.base import BaseSubclassRegister
from brane.core.utils import integrate_args, integrate_kwargs
from brane.core.base import MetaFalse
import importlib

class MetaModule(type):
    def __new__(cls, classname, bases, class_info):
        new_class_info = class_info.copy()
        if new_class_info.get("name", None) is None:
            new_class_info["name"] = new_class_info.get("module_name", None)
        print(f"[DEBUG]: in MetaModule class_info={new_class_info}")
        return type.__new__(cls, classname, bases, new_class_info)

class Module(ModuleClassType, BaseSubclassRegister, metaclass=MetaModule):
    # should be unqiue. package name specifed at pip install is usually set
    name: Optional[str] = None
    # module name for base. allow the string like "module1.module2"
    module_name: Optional[str] = None
    # the module specified by the module_name is set at load_modules method
    module: Any = None
    # temporal / experimental
    loaded: bool = False

    module_method_read: Optional[str] = None
    read_method: Callable = None

    module_method_write: Optional[str] = None
    write_method: Callable = None
    file_arg_first: bool = True

    file_open_for_read: bool = False
    open_mode_for_read: dict = {"mode": "r"}
    file_open_for_write: bool = False
    open_mode_for_write: dict = {"mode": "w"}

    object_method_write: Optional[str] = None### temporal arg name

    # temporal arg name # unnecessary ?
    require_file_stream_read = False

    base_args_read: tuple = ()
    base_kwargs_read: dict = {}
    base_args_write: tuple = ()
    base_kwargs_write: dict = {}
    generate_params_read = None # unnecessary ?
    generate_params_write = None
    
    @classmethod
    def load_modules(cls):
        # allow lazy loading of modules
        if cls.module_name:
            if cls.module is None:
                cls.module = importlib.import_module(cls.module_name)
        if cls.module_method_read:
            cls.read_method = getattr(cls.module, cls.module_method_read)
        else:
            raise ValueError("'module_method_read' is undefined")# [ARGS]: other error type ?
        if cls.module_method_write:
            cls.write_method = getattr(cls.module, cls.module_method_write)
        elif cls.object_method_write:
            pass
        else:
            raise ValueError("'module_method_write' is undefined")# [ARGS]: other error type ?

    @classmethod
    def read(cls, path: Optional[PathType] = None, file: Optional[FileType] = None, *args, **kwargs):
        # generate the args and keyword args passed to read method
        base_args_read, base_kwargs_read = cls.base_args_read, cls.base_kwargs_read.copy()
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
    def write(cls, obj: Any, path: Optional[PathType] = None, file: Optional[FileType] = None, *args, **kwargs):
        base_args_write, base_kwargs_write = cls.base_args_write, cls.base_kwargs_write.copy()
        if cls.generate_params_write:
            base_args_write, base_kwargs_write = cls.generate_params_write(obj, base_args_write, base_kwargs_write)
            
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
        
    #_registered_subclasses = []
    _registered_subclasses = {}
    registered_modules = _registered_subclasses
    # [ToDo]: define class-propetry or dynamical attibutes by using meta class
    #@property
    #def registered_modules(cls):
    #    return [ c for c in cls.__registered_subclasses if c != cls ]
    
    # def __init_subclass__(cls):
    #     #super().__init_subclass__()
    #     #super(cls).__class__.registered_modules.append(cls)
    #     #print(cls)
    #     if cls.valid:
    #         cls.registered_modules.append(cls)
    #     # これだと継承クラス全体でregistered_moduleをシェア
        
    #def __init__(self):
    #    self.registered_modules = []
    #def __init_subclass__(cls):
    #    print(super())
    #    super().registered_modules.append(cls)

    # # if False, not register the module
    # valid = True# temporal arg name
    # #@property
    # #def valid(self):
    # #    return self._valid

class MetaNoneModule(MetaModule, MetaFalse):# [MEMO]: deprecated after removing MetaModule
    pass

class NoneModule(Module, metaclass=MetaNoneModule):
    valid = False###
    name = "None"
    
    #@classmethod # not work for class
    #def __bool__(cls):
    #    return False
