from __future__ import annotations
from brane.typing import *
from brane.core.base import Context
from brane.core.mapper import Extension2Module, Extension2Format, ObjectFormat2Module
from brane.core.hook import FunctionHook, Hook
from brane.libs.events import BasicEvents
from brane.core.utils import get_extension_from_filname_default, integrate_args, integrate_kwargs
### temporal just activate class definitions
from brane.libs.modules import PILModule
from brane.libs.formats import TableType
from brane.libs.objects import PIL_Image_Object
from brane.libs.extensions import info
from pathlib import Path
# [ARG]: moved to hook.py ?

class HookManager(object):
    """ This is a temporal class.
    [ARGS]:
    * consider better class name
    * refactor this class
    """
    @classmethod
    def get_hook_class(cls, hook, **hook_kwargs):
        if isinstance(hook, Hook):
            return hook
        else:### detail check ?
            return FunctionHook(hook, **hook_kwargs)

    @classmethod
    def connect_hook_and_event(cls, event, hook, **hook_kwargs):
        hook = cls.get_hook_class(hook, **hook_kwargs)
        event.add_hooks(hook)

    @classmethod
    def register_read_pre_hook(cls, hook, **hook_kwargs):
        cls.connect_hook_and_event(BasicEvents.read_pre, hook, **hook_kwargs)

    @classmethod
    def register_read_post_hook(cls, hook, **hook_kwargs):
        cls.connect_hook_and_event(BasicEvents.read_post, hook, **hook_kwargs)

    @classmethod
    def register_write_pre_hook(cls, hook, **hook_kwargs):
        cls.connect_hook_and_event(BasicEvents.write_pre, hook, **hook_kwargs)

    @classmethod
    def register_write_post_hook(cls, hook, **hook_kwargs):
        cls.connect_hook_and_event(BasicEvents.write_post, hook, **hook_kwargs)

    @classmethod
    def register_read_all_post_hook(cls, hook, **hook_kwargs):
        func = FunctionHook(hook, container_type="list", **hook_kwargs)### temporal
        #ReadAllPostEvent.add_hooks(func)
        BasicEvents.readall_post.add_hooks(func)
        # use cls.connect_hook_and_event

    @classmethod
    def register_write_all_post_hook(cls, hook, **hook_kwargs):
        raise NotImplementedError

    @classmethod
    def clear_hooks(cls, event):
        event.clear_hooks()

    @classmethod
    def clear_read_pre_hook(cls):
        cls.clear_hooks(BasicEvents.read_pre)

    @classmethod
    def clear_read_post_hook(cls):
        cls.clear_hooks(BasicEvents.read_post)

    @classmethod
    def clear_write_pre_hook(cls):
        cls.clear_hooks(BasicEvents.write_pre)

    @classmethod
    def clear_write_post_hook(cls):
        cls.clear_hooks(BasicEvents.write_post)

    @classmethod
    def clear_read_all_post_hook(cls):
        raise NotImplementedError

    @classmethod
    def clear_write_all_post_hook(cls):
        raise NotImplementedError

class IOLogger(object):
    "v4.2"
    # for debug at this stage
    log = []

class IOManager(HookManager):
    """
    [ARGS]
    * refactor for better implementation
    * use mixin ?
    """

    get_extension_from_filename = get_extension_from_filname_default
    logger = IOLogger()
    
    @classmethod
    def read(cls, path, *args, **kwargs):# add args and kwargs
        ext = cls.get_extension_from_filename(path)
        #Fmt = Extension2Format.get_format(ext)
        #if Fmt is None:
        #    raise NotImplementedError(f"Cannot find the corresponding format for given extension {ext}")
        Mdl = Extension2Module.get_module(ext)
        if Mdl is None:
            raise NotImplementedError(f"Cannot find the corresponding module for given extension {ext}")
        Mdl.load_modules()

        #context = { "path": path, "ext": ext, "Format": Fmt }
        context: ContextInterface = Context({ "path": path, "ext": ext, "Module": Mdl })# add Fmt as supplementary ?
        context = BasicEvents.read_pre.fire(context)
        path = context["path"]
        base_args = context.get("args", ())
        base_kwargs = context.get("kwargs", {})
        base_args = integrate_args(base_args, args)
        base_kwargs = integrate_kwargs(base_kwargs, kwargs)

        cls.logger.log.append( { "path": path, "ext": ext, "module": Mdl.name, "args": args, "kwargs": kwargs } )
        obj = Mdl.read(file=path, *base_args, **base_kwargs)

        context.update({ "object": obj })
        context = BasicEvents.read_post.fire(context)
        obj = context["object"]
        return obj
    
    @classmethod
    def read_all_as_list(cls, multiple_paths: list[str], read_args: tuple = (), read_kwargs: dict = {}, *args, **kwargs):
        paths: list = []
        if isinstance(multiple_paths, str):
            import glob
            paths = glob.glob(multiple_paths, recursive=True)
        elif isinstance(multiple_paths, list):# [TODO]: include tuple ?
            assert all(map(lambda path: isinstance(path, str), multiple_paths))
            paths = multiple_paths
        else:
            raise NotImplementedError
        if len(paths) == 0:
            return {}

        context: ContextInterface = Context({ "paths": paths })
        context = BasicEvents.readall_pre.fire(context)
        objs = []
        for path in paths:
            obj = cls.read(path=path, *read_args, **read_kwargs)
            objs.append(obj)
        context.update({ "objects": objs })

        # experimental
        if "sort_func" in kwargs:
            sort_func = kwargs["sort_func"]
            context = sort_func(context)
        
        context = BasicEvents.readall_post.fire(context)
        if "object" in context:
            return context["object"]
        else:
            return context["objects"]

    @classmethod
    def read_all_as_dict(cls, multiple_paths: dict[str, str], read_args: tuple = (), read_kwargs: dict = {}, *args, **kwargs):
        paths: dict = {}
        if isinstance(multiple_paths, str):
            import glob
            paths = { path: path for path in glob.glob(multiple_paths, recursive=True) }
        elif isinstance(multiple_paths, list):
            assert all(map(lambda path: isinstance(path, str), multiple_paths))
            paths = { path: path for path in multiple_paths }
        elif isinstance(multiple_paths, dict):
            assert all(map(lambda path: isinstance(path, str), multiple_paths.values()))
            paths = multiple_paths
        else:
            raise NotImplementedError
        if len(paths) == 0:
            return {}

        context: ContextInterface = Context({ "paths": paths })
        context = BasicEvents.readall_pre.fire(context)
        objs = {}
        for key, path in paths.items():
            obj = cls.read(path=path, *read_args, **read_kwargs)# [ARG]: parameter 'file' (stream or path ?)
            objs.update({ key: obj })
        context.update({ "objects": objs })

        # experimental
        if "sort_func" in kwargs:
            sort_func = kwargs["sort_func"]
            context = sort_func(context)

        context = BasicEvents.readall_post.fire(context)
        if "object" in context:
            return context["object"]
        else:
            return context["objects"]

    @classmethod
    def write(cls, obj, path, *args, **kwargs):# [ARG]: addtional args: ext=None, 
        ext = cls.get_extension_from_filename(path)
        Fmt = Extension2Format.get_format(ext) if ext else None### replace NoneFormat
        Mdl = ObjectFormat2Module.get_module_from_object(obj, fmt=Fmt)
        if Mdl is None:
            raise NotImplementedError(f"Cannot find the corresponding module for given object type {type(obj)}")
        Mdl.load_modules()

        context: ContextInterface = Context({ "path": path, "object": obj, "Module": Mdl })
        context = BasicEvents.write_pre.fire(context)
        base_args = context.get("args", ())
        base_kwargs = context.get("kwargs", {})
        base_args = integrate_args(base_args, args)
        base_kwargs = integrate_kwargs(base_kwargs, kwargs)

        Mdl.write(obj=obj, file=path, *base_args, **base_kwargs)
        context = BasicEvents.write_post.fire(context)

    @classmethod
    def write_all_from_list(cls, obj_list: list, output_dir: Optional[PathType] = None, path_ruler = None,
                            write_args: tuple = (), write_kwargs: dict = {}, *args, **kwargs):
        # [ARG]: list case is the special case of dict, to say, the index can be seen as the key -> unify two ??
        # [TODO]: should allow the iterator...
        # path assignemtn option
        # 1. output_dir + str(idx)
        # 2. path_ruler(obj_list)
        # 3. output_dir + path_ruler(obj_list)
        if not isinstance(obj_list, list):# [NOTE]: This is used for dynamical check
            raise ValueError(f"obj_list should be python `list` but the actual type is {type(obj_list)}")# [TODO]: implement some function for value check

        paths: list[str, PathType] = []
        if output_dir is not None:
            if path_ruler is None:
                path_ruler = lambda idx: str(idx)
            paths = [ Path(output_dir) / path_ruler(idx) for idx in range(len(obj_list)) ]
        elif path_ruler is not None:
            paths = [ path_ruler(idx) for idx in range(len(obj_list)) ]
        else:
            raise ValueError("Either output_dir or path_ruler should not be None")

        context: ContextInterface = Context({ "paths": paths, "objects": obj_list })
        context = BasicEvents.writeall_pre.fire(context)
        for idx, obj in enumerate(obj_list):
            path = paths[idx]
            cls.write(obj=obj, path=path, *write_args, **write_kwargs)

        context = BasicEvents.writeall_post.fire(context)

    @classmethod
    def write_all_from_dict(cls, obj_dict: dict, output_dir: Optional[PathType] = None, path_ruler = None,
                            write_args: tuple = (), write_kwargs: dict = {}, *args, **kwargs):
        # path assignemtn option
        # 1. output_dir + key
        # 2. path_ruler(obj_dict)
        # 3. output_dir + path_ruler(obj_dict)
        if not isinstance(obj_dict, dict):# [NOTE]: This is used for dynamical check
            raise ValueError(f"obj_dict should be python `dict` but the actual type is {type(obj_dict)}")

        paths: dict[str, PathType] = {}
        if output_dir is not None:
            if path_ruler is None:
                path_ruler = lambda key: key
            paths = { key: Path(output_dir) / path_ruler(key) for key in obj_dict.keys() }
        elif path_ruler is not None:
            paths = { key: path_ruler(key) for key in obj_dict.keys() }
        else:
            raise ValueError("Either output_dir or path_ruler should not be None")

        context: ContextInterface = Context({ "paths": paths, "objects": obj_dict })
        context = BasicEvents.writeall_pre.fire(context)
        for key, obj in obj_dict.items():
            path = paths[key]
            cls.write(obj=obj, path=path, *write_args, **write_kwargs)

        context = BasicEvents.writeall_post.fire(context)
