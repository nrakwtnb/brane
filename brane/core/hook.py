from __future__ import annotations

from abc import ABCMeta, abstractmethod

from brane.typing import *  # noqa: F403


class Hook(HookClassType, metaclass=ABCMeta):
    hook_name: Optional[str] = None
    flag: HookFlagType = None  # other name convention: marker
    _active: bool = True

    def __init__(self, name: Optional[str] = None, flag: HookFlagType = None):
        self.hook_name: Optional[str] = name
        self.flag: HookFlagType = flag  # other name convention: marker
        self._active: bool = True

    def condition(self, info: ContextInterface) -> bool:
        return True

    @abstractmethod
    def __call__(self, info: ContextInterface) -> Union[ContextInterface, None]:
        raise NotImplementedError

    @property
    def active(self) -> bool:
        return self._active

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False

    def __repr__(self) -> str:
        if self.hook_name is not None:
            return self.hook_name


class FunctionHook(Hook):
    def __init__(
        self,
        func: Callable[ContextInterface, ContextInterface],
        condition_func: Callable[ContextInterface, bool] = lambda info: True,
        name: Optional[str] = None,
        flag: HookFlagType = None,
        **kwargs_exp
    ):
        """
        Args:
            func: hook function. It recevices context including path/paths, object/objects and return
            condition_func: evaluate  whether this hook is called or not based on the context.
            name:
            flag:

            # experimental keyword aruguments
            skip_when_error:
            object_type (type):
            container_type (None|'list'|'tuple'|'dict'):
            is_multiple_objects (bool):
        """
        super().__init__(name=name, flag=flag)
        self.hook_func = func

        if "skip_when_error" in kwargs_exp:
            self.skip_when_error = kwargs_exp["skip_when_error"]  # not used yet

        if "object_type" in kwargs_exp:
            target_object_type: type = kwargs_exp["object_type"]
            # container_type = kwargs_exp.get("container_type", None)
            # is_multiple_objects: bool = kwargs_exp.get("is_multiple_objects", False)
            # [ARG]: should use higher order function ?
            def check_object_type(obj: Any) -> bool:
                # nonlocal target_object_type
                return isinstance(obj, target_object_type)

            # if is_multiple_objects:
            def new_condition(info: ContextInterface) -> bool:
                obj = info.get("object", None)
                objs = info.get("objects", None)
                if objs is None and obj is not None:
                    return check_object_type(obj) and condition_func(info)
                if objs is not None and obj is None:
                    if isinstance(objs, list) or isinstance(objs, tuple):
                        return all(map(check_object_type, objs)) and condition_func(info)
                    elif isinstance(objs, dict):
                        return all(map(check_object_type, objs.values())) and condition_func(info)
                    else:
                        raise NotImplementedError(type(objs))
                else:
                    raise AssertionError()

            # if container_type == "sequence":
            #    def new_condition(info: ContextInterface) -> bool:
            #        objs = info.get("objects", None)
            #        container_type_check = isinstance(objs, list) or isinstance(objs, tuple)
            #        return container_type_check and all(map(check_object_type, objs)) and condition_func(info)
            # elif container_type == "mapping":
            #    def new_condition(info: ContextInterface) -> bool:
            #        objs = info.get("objects", None)
            #        container_type_check = isinstance(objs, dict)
            #        return container_type_check and all(map(check_object_type, objs.values())) and condition_func(info)
            # else:
            #    def new_condition(info: ContextInterface) -> bool:
            #        # info = { "object": obj, ... }
            #        obj = info.get("object", None)
            #        return check_object_type(obj) and condition_func(info)
            self.condition_func = new_condition
        else:
            self.condition_func = condition_func

    def __call__(self, info: ContextInterface) -> ContextInterface:
        return self.hook_func(info)

    def condition(self, info: ContextInterface) -> bool:
        return self.condition_func(info)

    def __repr__(self) -> str:
        if self.hook_name is not None:
            return self.hook_name
        else:
            return repr(self.hook_func)
