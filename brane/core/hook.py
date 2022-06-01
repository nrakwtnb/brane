from __future__ import annotations
from brane.typing import *
from brane.core.base import Context

HookFlagType = Optional[Union[str, set[str]]]

class Hook(HookClassType):
    hook_name: Optional[str] = None
    flag: HookFlagType = None # other name convention: marker
    _active: bool = True
    def __init__(self, name: str = None):
        self.hook_name: Optional[str] = name
        self.flag: HookFlagType = None # other name convention: marker
        self._active: bool = True

    def condition(self, info: ContextInterface) -> bool:
        return True

    def __call__(self, info: ContextInterface) -> ContextInterface:
        raise NotImplementedError
    
    @property
    def active(self) -> bool:
        return self._active

    #def __repr__(self) -> str:
    #    if self.hook_name is not None:
    #        return self.hook_name
    #    else:
    #        return ""

class FunctionHook(Hook):
    def __init__(self, func, condition_func=lambda info: True, name=None, **kwargs_exp):
        """

        kwargs_exp: experimental keyword aruguments
        * skip_wehn_error
        * object_type
        """
        super().__init__(name)
        self.hook_func = func
        #self.hook_name = name
        #self.condition_func = condition_func

        if "skip_when_error" in kwargs_exp:
            self.skip_when_error = kwargs_exp["skip_when_error"]# not used yet

        if "object_type" in kwargs_exp:
            target_object_type = kwargs_exp["object_type"]
            container_type = kwargs_exp.get("container_type", None)
            def check_object_type(obj):### [ARG]: should use higher order function ?
                # nonlocal target_object_type
                return isinstance(obj, target_object_type)

            if container_type == "list":
                def new_condition(info: ContextInterface):
                    objs = info.get("objects", None)
                    container_type_check = isinstance(objs, list)
                    return container_type_check and all(map(check_object_type, objs)) and condition_func(info)
            elif container_type == "tuple":
                raise NotImplementedError
            elif container_type == "dict":
                raise NotImplementedError
            else:
                def new_condition(info: ContextInterface):
                    # info = { "object": obj, ... }
                    obj = info.get("object", None)
                    return check_object_type(obj) and condition_func(info)
            self.condition_func = new_condition
        else:
            self.condition_func = condition_func

    def __call__(self, info: ContextInterface):
        return self.hook_func(info)
    
    def condition(self, info: ContextInterface) -> bool:
        return self.condition_func(info)

    def __repr__(self) -> str:
        if self.hook_name is not None:
            return self.hook_name
        else:
            return repr(self.hook_func)
