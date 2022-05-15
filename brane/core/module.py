from __future__ import annotations
from brane.typing import *
from brane.core.base import BaseSubclassRegister
from brane.core.utils import integrate_args, integrate_kwargs

class Module(ModuleClassType, BaseSubclassRegister):
    name: Optional[str] = None
    module: Any = None
    loaded: bool = False

    base_args_read: tuple = ()
    base_kwargs_read: dict = {}
    base_args_write: tuple = ()
    base_kwargs_write: dict = {}
    generate_params_read = None # unnecessary ?
    generate_params_write = None
    
    module_method_read = None
    module_method_write = None
    swap_args: bool = None### temporal arg name
    object_method_write : str = None### temporal arg name
    
    require_file_stream_read = False# temporal arg name # unnecessary ?

    # # if False, not register the module
    # valid = True# temporal arg name
    # #@property
    # #def valid(self):
    # #    return self._valid

    #def load_modules(cls):
    @classmethod
    def load_modules(cls):
        # allow lazy loading of modules
        pass
        # raise NotImplementedError

    @classmethod
    def read(cls, file, *args, **kwargs):
        # generate the args and keyword args passed to read method
        base_args_read, base_kwargs_read = cls.base_args_read, cls.base_kwargs_read.copy()
        # [ARG]: unnecessary
        # if cls.generate_params_read:
        #     base_args_read, base_kwargs_read = cls.generate_params_read(base_args_read, base_kwargs_read)

        args_read = integrate_args(base_args_read, args)
        kwargs_read = integrate_kwargs(base_kwargs_read, kwargs)
        # ToDo: args and kwargs -> ???

        # read
        if cls.module_method_read:
            return cls.module_method_read(file, *args_read, **kwargs_read)
        else:
            raise NotImplementedError

    @classmethod
    def write(cls, obj, file, *args, **kwargs):
        base_args_write, base_kwargs_write = cls.base_args_write, cls.base_kwargs_write.copy()
        if cls.generate_params_write:
            base_args_write, base_kwargs_write = cls.generate_params_write(obj, base_args_write, base_kwargs_write)
            
        args_write = integrate_args(base_args_write, args)
        kwargs_write = integrate_kwargs(base_kwargs_write, kwargs)
        
        
        if cls.module_method_write:
            if cls.swap_args:
                cls.module_method_write(file, obj, *args_write, **kwargs_write)
            else:
                cls.module_method_write(obj, file, *args_write, **kwargs_write)
        elif cls.object_method_write and hasattr(obj, cls.object_method_write):
            getattr(obj, cls.object_method_write)(file, *args_write, **kwargs_write)
        else:
            raise NotImplementedError
        
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
from brane.core.base import MetaFalse

class NoneModule(Module, metaclass=MetaFalse):
    valid = False###
    name = "None"
    
    #@classmethod # not work for class
    #def __bool__(cls):
    #    return False
