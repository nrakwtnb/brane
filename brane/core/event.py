from __future__ import annotations

from brane.typing import *  # noqa: F403

MultipleHookClassType = Union[
    HookClassType,
    list[HookClassType],
    tuple[HookClassType],
    set[HookClassType],
]


def convert_obj_into_list(obj) -> list:  # [ARG]: convert_iterator ?
    if isinstance(obj, list):
        return list(obj)
    elif isinstance(obj, tuple):
        return list(obj)
    elif isinstance(obj, set):
        return list(obj)
    else:
        return [obj]


class Event(EventClassType):
    # [TODO]: fix flag's specification
    # * and/or
    # * allow/denied

    # def __new__(cls):
    #    self = super().__new__(cls)### temporal ?
    #    EventManager.add_events(self)
    #    return self

    def __init__(self, event_name: str = "", hook_funcs: Optional[MultipleHookClassType] = None):
        self.hooks: list[HookClassType] = []
        if hook_funcs:
            self.hooks = convert_obj_into_list(hook_funcs)
        self.event_name: str = event_name
        self.allowed_flags: HookFlagType = None  # fixed in the future
        self.denied_flags: HookFlagType = None  # fixed in the future

    # @classmethod
    def add_hooks(self, hook_funcs: MultipleHookClassType):
        hook_funcs = convert_obj_into_list(hook_funcs)
        print(f"[DEBUG]: add {hook_funcs} at {self}")
        self.hooks.extend(hook_funcs)

    # @classmethod
    def clear_hooks(self):
        self.hooks = []

    def check_flag(self, flag: HookFlagType) -> bool:
        if flag is None:
            flag = set()
        elif isinstance(flag, str):
            flag = set(flag)
        if not isinstance(flag, set):  # flag \in set[str]
            raise AssertionError(type(flag))
        # [TODO]: implement
        return True

    # @classmethod
    def fire(self, info: ContextInterface, verbose: bool = False) -> ContextInterface:
        for hook in self.hooks:
            # [TODO]: use wallus operator in the future when supporting python>=3.8
            called: bool = False
            if hook.active and self.check_flag(hook.flag) and hook.condition(info):
                called = True
                # temporal
                # [TODO]: (very important) refine the specification and the logic
                res = hook(info)
                # if isinstance(res, dict): => if hook.return_as_context: (because it is not true for object is dict)
                #    info.update(res)
                # elif res is None:
                if res is None:
                    pass
                else:
                    info.update({"object": res})
            if verbose:
                active_: bool = self.active
                if not active_:
                    print(f"skipped '{hook.hook_name}': non-active")
                    continue
                flag_check_: bool = self.check_flag(hook.flag)
                if not flag_check_:
                    print(f"skipped '{hook.hook_name}': out of flags")
                    continue
                if called:
                    print(f"called '{hook.hook_name}'")
                else:
                    # [ARG]: allow us to access the reason why this is not satisfied ?
                    print(f"skipped '{hook.hook_name}': out of conditions")
        return info

    def __repr__(self) -> str:
        return "\n".join([f"{i}. {repr(hook)}" for i, hook in enumerate(self.hooks, start=1)])
