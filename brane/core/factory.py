from __future__ import annotations

import os
from pathlib import Path

import yaml

from brane.core.format import Format
from brane.core.module import Module
from brane.core.object import Object
from brane.typing import *  # noqa: F403

CORE_MODULE_CONFIG_PATH: Path = (Path(__file__) / "../../../" / "./config/modules/core.yaml").resolve()
THIRDPARTY_MODULE_CONFIG_PATH: Path = (Path(__file__) / "../../../" / "./config/modules/basic.yaml").resolve()
CORE_FORMAT_CONFIG_PATH: Path = (Path(__file__) / "../../../" / "./config/formats/core.yaml").resolve()
THIRDPARTY_FORMAT_CONFIG_PATH: Path = (Path(__file__) / "../../../" / "./config/formats/basic.yaml").resolve()
CORE_OBJECT_CONFIG_PATH: Path = (Path(__file__) / "../../../" / "./config/objects/core.yaml").resolve()
THIRDPARTY_OBJECT_CONFIG_PATH: Path = (Path(__file__) / "../../../" / "./config/objects/basic.yaml").resolve()

ClassAttributeType = dict[str, Any]
ConfigType = dict[str, Union[str, dict]]


class Factory(object):
    className2Module: dict[str, ModuleClassType] = dict()
    className2Format: dict[str, FormatClassType] = dict()
    className2Object: dict[str, ObjectClassType] = dict()
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Factory, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.activate()

    @staticmethod
    def load_config(config_path: str) -> ConfigType:
        cfg: ConfigType = {}
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                cfg = yaml.safe_load(f)
        return cfg

    @staticmethod
    def generate_classes_from_configs(
        config_list: list[ConfigType],
        suffix: str,
        cls: type,
        apply_attributes: Optional[Callable[[str, ClassAttributeType], ClassAttributeType]] = None,
    ) -> dict[str, type]:
        name2class: dict[str, type] = {}
        for config in config_list:
            name2class_for_cfg: dict[str, type] = {
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
    def load_brane_modules(cls) -> dict[str, ModuleClassType]:
        cfg_core = cls.load_config(config_path=CORE_MODULE_CONFIG_PATH)
        cfg_thirdparty = Factory.load_config(config_path=THIRDPARTY_MODULE_CONFIG_PATH)

        className2Module = cls.generate_classes_from_configs(
            config_list=[cfg_core, cfg_thirdparty], suffix="Module", cls=Module, apply_attributes=None
        )
        return className2Module

    @classmethod
    def load_brane_formats(cls) -> dict[str, FormatClassType]:
        cfg_core = Factory.load_config(config_path=CORE_FORMAT_CONFIG_PATH)
        cfg_thirdparty = Factory.load_config(config_path=THIRDPARTY_FORMAT_CONFIG_PATH)

        def update_attributes(class_name: str, attributes: ClassAttributeType) -> ClassAttributeType:
            attributes = attributes.copy()
            if attributes.get("name", None):
                attributes["name"] = class_name

            if attributes.get("module", None) is None and attributes.get("module_name", None) is not None:
                attributes["module"] = cls.className2Module.get(attributes["module_name"], None)

            if attributes["module"] is None:
                if attributes["module_name"]:
                    print(f"[WARNING]: module name {attributes['module_name']} is not found")
                    # raise AssertionError(f"module name {attributes['module_name']} is not found")
                else:
                    print(f"[WARNING]: module name is not defined for {attributes.get('name', '')}")

            return attributes

        className2Format = cls.generate_classes_from_configs(
            config_list=[cfg_core, cfg_thirdparty], suffix="Format", cls=Format, apply_attributes=update_attributes
        )
        return className2Format

    @classmethod
    def load_brane_objects(cls) -> dict[str, ObjectClassType]:
        cfg_core = Factory.load_config(config_path=CORE_OBJECT_CONFIG_PATH)
        cfg_thirdparty = Factory.load_config(config_path=THIRDPARTY_OBJECT_CONFIG_PATH)

        def update_attributes(class_name: str, attributes: ClassAttributeType) -> ClassAttributeType:
            attributes = attributes.copy()
            if attributes.get("name", None):
                attributes["name"] = class_name

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

        className2Object = cls.generate_classes_from_configs(
            config_list=[cfg_core, cfg_thirdparty], suffix="_Object", cls=Object, apply_attributes=update_attributes
        )
        return className2Object

    @classmethod
    def activate(cls, config_path: Optional[PathType] = None):
        cls.className2Module = cls.load_brane_modules()
        cls.className2Format = cls.load_brane_formats()
        cls.className2Object = cls.load_brane_objects()
