from __future__ import annotations
from brane.typing import *
from brane.core.hook import Hook

#HookFuncType = Hook
ObjOrMultipleTypeGenerator = lambda T: Union[T, List[T], Tuple[T], Set[T]] # [ARG]: better name ?

def convert_obj_into_list(obj) -> list:# convert_iterator ?
    if isinstance(obj, list):
        return list(obj)
    elif isinstance(obj, tuple):
        return list(obj)
    elif isinstance(obj, set):
        return list(obj)
    else:
        return [obj]


class Event(EventClassType):
    #def __new__(cls):
    #    self = super().__new__(cls)### temporal ?
    #    EventManager.add_events(self)
    #    return self

    def __init__(self, event_name: str = "", hook_funcs: Optional[ObjOrMultipleTypeGenerator(HookClassType)] = None):
        if hook_funcs:
            self.hooks = convert_obj_into_list(hook_funcs)
        else:
            self.hooks = []
        self.event_name = event_name

    #def add_hook_func(self, hook_funcs: ObjOrMultipleTypeGenerator(HookFuncType)):
    #@classmethod
    def add_hooks(self, hook_funcs: ObjOrMultipleTypeGenerator(HookClassType)):
        hook_funcs = convert_obj_into_list(hook_funcs)
        #self.hooks.extend(hook_funcs)
        self.hooks.extend(hook_funcs)

    #@classmethod
    def clear_hooks(self):
        self.hooks = []

    def check_flag(self, flag: Optional[Union[str, set(str)]]) -> bool:
        if flag is None:
            flag = set()
        elif isinstance(flag, str):
            flag = set(flag)
        # [TODO]: implement
        return True

    #def call_hooks(hooks, info):
    #def fire(self, info):
    #@classmethod
    def fire(self, info: ContextInterface):
        #for hook in self.hooks:
        for hook in self.hooks:
            if hook.active and self.check_flag(hook.flag) and hook.condition(info):
                res = hook(info)
                #if isinstance(res, dict): => if hook.return_as_context: (because it is not true for object is dict)
                #    info.update(res)
                #elif res is None:
                if res is None:
                    pass
                else:
                    info.update({ "object": res })
        return info
    
    def __repr__(self):
        return "\n".join([ f"{i}. {repr(hook)}" for i, hook in enumerate(self.hooks, start=1) ])
