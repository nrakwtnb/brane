from __future__ import annotations

import importlib
import os
from pathlib import Path

import yaml

import brane.config as default_cfg
from brane.core.format import FormatTemplate
from brane.core.module import ModuleTemplate
from brane.core.object import ObjectTemplate
from brane.typing import *  # noqa: F403

ClassAttributeType = NewType('ClassAttributeType', dict[str, Any])
# ConfigType = NewType('ConfigType', dict[str, Union[str, dict]])
ConfigType = dict[str, Union[str, dict]]


class ModuleConfigType(dict[str, dict[str, Any]]):
    pass


class FormatConfigType(dict[str, dict[str, Any]]):
    pass


class ObjectConfigType(dict[str, dict[str, Any]]):
    pass


class HookConfigType(ConfigType):
    pass


def load_config(config_path: PathType, strict: bool = False) -> ConfigType:
    cfg: ConfigType = {}
    # if os.path.exists(str(config_path)):  [ARG]: which to use
    if Path(config_path).exists():
        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)
    else:
        if strict:
            raise FileNotFoundError(config_path)
    return cfg


def load_multiple_config(config_path_list: list[PathType], strict: bool = False) -> list[ConfigType]:
    return [load_config(config_path, strict=strict) for config_path in config_path_list]


T = TypeVar('T')


class BraneClassGenerator(object):  # [ARG]: rename class name ?
    # [TODO]: verify config format based on Config class
    className2Module: dict[str, ModuleClassType] = dict()
    className2Format: dict[str, FormatClassType] = dict()
    className2Object: dict[str, ObjectClassType] = dict()
    _instance = None

    def __new__(cls):
        # Singleton pattern
        if cls._instance is None:
            cls._instance = super(BraneClassGenerator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.setup()

    @staticmethod
    def generate_classes_from_configs(
        config_list: list[ConfigType],
        suffix: str,
        cls: T,
        apply_attributes: Optional[Callable[[str, ClassAttributeType], ClassAttributeType]] = None,
    ) -> dict[str, T]:
        # [TODO]: use generics: type of return's value can be of ModuleClassType, FormatClassType or ObjectClassType depending on cls
        name2class: dict[str, type] = {}
        for config in config_list:
            name2class_for_cfg: dict[str, type] = {
                # getattr(attributes, "name") if hasattr(attributes, "name") else class_name.lower(): type(
                class_name: type(
                    f"{class_name}{suffix}",
                    (cls,),
                    apply_attributes(class_name, attributes) if apply_attributes else attributes,
                )
                for class_name, attributes in config.items()
            }
            name2class.update(name2class_for_cfg)
        return name2class

    @classmethod
    def load_brane_modules(cls, config_path_list: list[PathType]) -> dict[str, ModuleClassType]:
        def update_attributes(class_name: str, attributes: ClassAttributeType) -> ClassAttributeType:
            # nonlocal cls
            attributes = attributes.copy()
            if not attributes.get("name", None):
                attributes["name"] = class_name.lower()

            return attributes

        config_list: list[ConfigType] = load_multiple_config(config_path_list=config_path_list)
        # [TODO]: config verification: each is of ModuleConfigType ?
        className2Module: dict[str, ModuleClassType] = cls.generate_classes_from_configs(
            config_list=config_list, suffix="Module", cls=ModuleTemplate, apply_attributes=update_attributes
        )
        return className2Module

    @classmethod
    def load_brane_formats(cls, config_path_list: list[PathType]) -> dict[str, FormatClassType]:
        def update_attributes(class_name: str, attributes: ClassAttributeType) -> ClassAttributeType:
            # nonlocal cls
            attributes = attributes.copy()
            if not attributes.get("name", None):
                attributes["name"] = class_name.lower()

            if attributes.get("module", None) is None and attributes.get("module_name", None) is not None:
                attributes["module"] = cls.className2Module.get(attributes["module_name"], None)

            if attributes["module"] is None:
                if attributes["module_name"]:
                    print(f"[WARNING]: module name {attributes['module_name']} is not found")
                    # raise AssertionError(f"module name {attributes['module_name']} is not found")
                else:
                    print(f"[WARNING]: module name is not defined for {attributes.get('name', '')}")

            return attributes

        config_list: list[ConfigType] = load_multiple_config(config_path_list=config_path_list)
        # [TODO]: config verification: each is of FormatConfigType ?
        className2Format: dict[str, FormatClassType] = cls.generate_classes_from_configs(
            config_list=config_list, suffix="Format", cls=FormatTemplate, apply_attributes=update_attributes
        )
        return className2Format

    @classmethod
    def load_brane_objects(cls, config_path_list: list[PathType]) -> dict[str, ObjectClassType]:
        def update_attributes(class_name: str, attributes: ClassAttributeType) -> ClassAttributeType:
            # nonlocal cls
            attributes = attributes.copy()
            if not attributes.get("name", None):
                attributes["name"] = class_name.lower()

            if attributes.get("format", None) is None and attributes.get("format_name", None) is not None:
                attributes["format"] = cls.className2Format.get(attributes["format_name"], None)
            if attributes.get("module", None) is None and attributes.get("module_name", None) is not None:
                attributes["module"] = cls.className2Module.get(attributes["module_name"], None)

            if attributes["module"] is None:
                if attributes["module_name"]:
                    print(f"[WARNING]: module name {attributes['module_name']} is not found")
                    # raise AssertionError(f"module name {attributes['module_name']} is not found")
                else:
                    print(f"[WARNING]: module name is not defined for {attributes.get('name', '')}")

            if attributes["format"] is None:
                if attributes["format_name"]:
                    print(f"[WARNING]: format name {attributes['format_name']} is not found")
                    # raise AssertionError(f"format name {attributes['format_name']} is not found")
                else:
                    print(f"[WARNING]: format name is not defined for {attributes.get('name', '')}")

            return attributes

        config_list: list[ConfigType] = load_multiple_config(config_path_list=config_path_list)
        # [TODO]: config verification: each is of ObjectConfigType ?
        className2Object: dict[str, ObjectClassType] = cls.generate_classes_from_configs(
            config_list=config_list, suffix="_Object", cls=ObjectTemplate, apply_attributes=update_attributes
        )
        return className2Object

    @classmethod
    def setup(
        cls,
        module_config_paths: Optional[list[PathType]] = None,
        format_config_paths: Optional[list[PathType]] = None,
        object_config_paths: Optional[list[PathType]] = None,
    ):
        if module_config_paths is None:
            module_config_paths = default_cfg.MODULE_CONFIGS
        if format_config_paths is None:
            format_config_paths = default_cfg.FORMAT_CONFIGS
        if object_config_paths is None:
            object_config_paths = default_cfg.OBJECT_CONFIGS

        cls.className2Module = cls.load_brane_modules(config_path_list=module_config_paths)
        cls.className2Format = cls.load_brane_formats(config_path_list=format_config_paths)
        cls.className2Object = cls.load_brane_objects(config_path_list=object_config_paths)

    @classmethod
    def activate(
        cls,
        module_config_paths: Optional[list[PathType]] = None,
        format_config_paths: Optional[list[PathType]] = None,
        object_config_paths: Optional[list[PathType]] = None,
    ):
        # [MEMO]: add new brane classes based on the specified configs
        raise NotImplementedError


LoadedHookType = Union[Callable, HookClassType]


class BraneHooksGenerator(object):
    event2hooks: dict[str, list] = dict()
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BraneHooksGenerator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.setup()

    @classmethod
    def _check_config(cls, cfg: ConfigType):
        if "version" not in cfg:
            raise ValueError("Invalid config")  # [TODO]: refine error

        if "targets" not in cfg:
            raise ValueError("Invalid config")  # [TODO]: refine error

    @staticmethod
    def _generate_hooks_from_config_for_dev0(cfg: ConfigType) -> dict[str, list[LoadedHookType]]:
        # [TODO]: reduce the depth of nested for-and-if-statements
        # [TODO]: allow Functionhook arguments (flg, condition, ...)
        loaded_hooks: dict[str, list[LoadedHookType]] = {}
        for event, target_hook_list in cfg["targets"].items():
            if target_hook_list is None:
                continue
            loaded_hooks_for_event: list[LoadedHookType] = []
            for module2hooks in target_hook_list:
                for module_name, hook_info_list in module2hooks.items():
                    module = importlib.import_module(module_name)
                    for hook_info in hook_info_list:

                        if isinstance(hook_info, str):
                            if hasattr(module, hook_info):
                                hook_func: Callable = getattr(module, hook_info)
                                loaded_hooks_for_event.append(hook_func)
                            else:
                                print(f"[WARNING]: no {hook_info} is found in {module}")

                        elif isinstance(hook_info, dict) and len(hook_info) == 1:
                            hook_class_name, hook_params = next(iter(hook_info.items()))
                            if hasattr(module, hook_class_name):
                                hook_class: HookClassType = getattr(module, hook_class_name)
                                if hook_params is None:
                                    loaded_hooks_for_event.append(hook_class())
                                elif isinstance(hook_params, dict):
                                    loaded_hooks_for_event.append(hook_class(**hook_params))
                                else:
                                    print(
                                        f"[WARNING]: hook argument should be of dict or None. {hook_params} is not so."
                                    )
                            else:
                                print(f"[WARNING]: no {hook_class} is found in {module}")

                        else:
                            raise NotImplementedError(f"Invalid hook info: {hook_info}")  # [TODO]: refine error
            loaded_hooks[event] = loaded_hooks_for_event
        return loaded_hooks

    @classmethod
    def load_hooks_from_config(cls, config_path: PathType) -> dict[str, list[LoadedHookType]]:
        cfg: ConfigType = load_config(config_path)
        cls._check_config(cfg)
        cfg_version: str = cfg["version"]
        if cfg_version == "dev.0":
            return cls._generate_hooks_from_config_for_dev0(cfg=cfg)
        else:
            raise NotImplementedError(f"Unsupported hook config version: {cfg_version}")  # [TODO]: refine error

    @classmethod
    def load_event2hooks(cls, config_paths: Optional[list[PathType]] = None) -> dict[str, list[LoadedHookType]]:
        if config_paths is None:
            config_paths = []

        event2hooks: dict[str, list[LoadedHookType]] = dict()
        for path in config_paths:
            if not os.path.exists(str(path)):
                continue
            event2hooks_for_cfg: dict[str, list[LoadedHookType]] = cls.load_hooks_from_config(config_path=path)
            for event, hooks in event2hooks_for_cfg.items():
                event2hooks.setdefault(event, []).extend(hooks)
        return event2hooks

    @classmethod
    def setup(cls, config_paths: Optional[list[PathType]] = None, use_builtin_config: bool = True):
        """Overwrite the base hook set based on the config."""
        all_config_paths: list[PathType] = []
        if use_builtin_config:
            all_config_paths.extend(default_cfg.HOOK_CONFIGS)
        if config_paths:
            all_config_paths.extend(config_paths)

        cls.event2hooks = cls.load_event2hooks(config_paths=all_config_paths)

    @classmethod
    def activate(cls, config_paths: Optional[list[PathType]]):
        # [MEMO]: add new hooks based on the specified configs
        raise NotImplementedError
