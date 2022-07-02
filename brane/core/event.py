from __future__ import annotations

import builtins
import dataclasses

from brane.core.utils import sort_mapper
from brane.typing import *  # noqa: F403

MultipleHookClassType = Union[
    HookClassType,
    list[HookClassType],
    tuple[HookClassType],
    set[HookClassType],
]
T = TypeVar('T')


def convert_obj_into_list(
    obj: Union[list[T], tuple[T], set[T], T]
) -> list[T]:  # [ARG]: convert_iterator ? and better typing ?
    if isinstance(obj, list):
        return list(obj)
    elif isinstance(obj, tuple):
        return list(obj)
    elif isinstance(obj, set):
        return list(obj)
    else:
        return [obj]


@dataclasses.dataclass
class MarkerRule:  # [ARG]: use TypedDict, namedtuple or dataclass
    # name: Union[str, int]
    marker: str
    action: Literal['allowed', 'denied']  # [TODO]: rename the field name
    priority: int


class Event(EventClassType):
    # [TODO]: fix marker's specification
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
        self.marker_rules: dict[Union[str, int], MarkerRule] = {}
        # self.allowed_markers: HookMarkerType = None  # fixed in the future
        # self.denied_markers: HookMarkerType = None  # fixed in the future

    def __len__(self) -> int:
        return len(self.hooks)

    def get_hook_names(self, exclude_none: bool = True) -> list[Optional[str]]:
        return [hook.hook_name for hook in self.hooks if not exclude_none or hook.hook_name is not None]

    def search_hook_name_with_index(self, target_name: str, exact: bool = False) -> tuple[int, str]:
        if exact:
            name_with_target = [
                (idx, name)
                for idx, name in enumerate(self.get_hook_names(exclude_none=True))
                if name is not None and name == target_name
            ]
        else:
            # mypy error: List comprehension has incompatible type List[Tuple[int, Optional[str]]]; expected List[Tuple[int, str]]
            name_with_target = [
                (idx, name)
                for idx, name in enumerate(self.get_hook_names(exclude_none=True))
                if name is not None and name.startswith(target_name)
            ]
        if len(name_with_target) == 0:
            raise ValueError("No match.")
        elif len(name_with_target) == 1:
            return next(iter(name_with_target))
        else:
            raise ValueError("Not unique.")

    # @classmethod
    def add_hooks(
        self,
        hook_funcs: MultipleHookClassType,
        ref_index: Optional[int] = None,
        ref_name: Optional[str] = None,
        loc: Literal['before', 'after'] = 'after',
    ):
        num_registered_hooks = len(self.hooks)
        if ref_name:
            ref_index, _ = self.search_hook_name_with_index(target_name=ref_name, exact=False)
        elif ref_index is None:
            ref_index = num_registered_hooks
        elif -num_registered_hooks <= ref_index < 0:
            ref_index += num_registered_hooks
        elif 0 <= ref_index <= num_registered_hooks:
            pass
        else:
            raise ValueError(
                f"`ref_index` should be between {-num_registered_hooks} and {num_registered_hooks} but actually {ref_index}"
            )

        hook_funcs = convert_obj_into_list(hook_funcs)
        print(f"[DEBUG]: add {hook_funcs} at {self}")
        if loc == 'before':
            hooks_former = self.hooks[:ref_index]
            hooks_latter = self.hooks[ref_index:]
        elif loc == 'after':
            hooks_former = self.hooks[: ref_index + 1]
            hooks_latter = self.hooks[ref_index + 1 :]
        else:
            raise AssertionError(loc)
        self.hooks = hooks_former + hook_funcs + hooks_latter

    # @classmethod
    def remove_hooks(self, hook_names: Union[str, Container[str]], strict: bool = False):
        # [MEMO]: When strict = True, it requires all the hook id should appear exactly once
        if strict:
            raise NotImplementedError

        if isinstance(hook_names, str):
            hook_names = [hook_names]

        def check_no_inclusion_of_hook_name(hook: HookClassType) -> bool:
            nonlocal hook_names
            return hook.hook_name not in hook_names

        new_hooks = list(filter(check_no_inclusion_of_hook_name, self.hooks))
        self.hooks = new_hooks

    # @classmethod
    def clear_hooks(self):
        self.hooks = []

    def add_marker_rule(
        self, name: Union[str, int], marker: str, action: Literal['allowed', 'denied'], priority: Optional[int] = None
    ):
        # [TODO]: automatic name assignment
        if name in self.marker_rules:
            raise KeyError(name)  # [TODO]: define KeyExistenceError or add new arg to ignore / replace
        priority_list = [rule.priority for rule in self.marker_rules.values()]
        if priority is None:
            priority = min(priority_list, default=10) - 10
        elif priority in priority_list:
            raise ValueError(priority)  # [TODO]; define PriorityOverkapError

        self.marker_rules.update({name: MarkerRule(marker=marker, action=action, priority=priority)})
        self.marker_rules = sort_mapper(mapper=self.marker_rules, key="priority")

    def remove_marker_rule(self, name: Union[str, int]) -> MarkerRule:
        return self.marker_rules.pop(name)

    def clean_marker_rules(self):
        self.marker_rules = dict()

    def check_marker(self, marker: HookMarkerType) -> bool:
        if marker is None:
            marker = set()
        elif isinstance(marker, str):
            marker = set(marker)

        for name, rule in self.marker_rules.items():
            if rule.marker in marker:
                if rule.action == 'allowed':
                    return True
                elif rule.action == 'denied':
                    return False
                else:
                    raise NotImplementedError()  # This error is not checked when typining is completed
        return True

    # @classmethod
    def fire(self, info: ContextInterface, verbose: bool = False) -> ContextInterface:
        for hook in self.hooks:
            # [TODO]: use wallus operator in the future when supporting python>=3.8
            called: bool = False
            if hook.active and self.check_marker(hook.marker) and hook.condition(info):
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
                if not hook.active:
                    builtins.print(f"skipped '{hook.hook_name}': non-active")
                    continue
                marker_check_: bool = self.check_marker(hook.marker)
                if not marker_check_:
                    builtins.print(f"skipped '{hook.hook_name}': out of markers")
                    continue
                if called:
                    builtins.print(f"called '{hook.hook_name}'")
                else:
                    # [ARG]: allow us to access the reason why this is not satisfied ?
                    builtins.print(f"skipped '{hook.hook_name}': out of conditions")
        return info

    def __repr__(self) -> str:
        return "\n".join([f"{i}. {repr(hook)}" for i, hook in enumerate(self.hooks, start=1)])
