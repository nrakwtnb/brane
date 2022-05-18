from __future__ import annotations
from brane.typing import *
from brane.core.module import Module
CORE_MODULE_CONFIG_PATH = "./config/modules/core.yaml"
THIRDPARTY_MODULE_CONFIG_PATH = "./config/modules/basic.yaml"
import yaml

def load_brane_modules():
    with open(CORE_MODULE_CONFIG_PATH, "r") as f:
        cfg_core: dict = yaml.safe_load(f)

    with open(THIRDPARTY_MODULE_CONFIG_PATH, "r") as f:
        cfg_thirdparty: dict = yaml.safe_load(f)

    className2Module: dict[str, type] = {
        **{
            class_name: type(f"{class_name}Module", (Module, ), attributes)
            for class_name, attributes in cfg_core.items()
        },
        **{
            class_name: type(f"{class_name}Module", (Module, ), attributes)
            for class_name, attributes in cfg_thirdparty.items()
        }
    }
    return className2Module

className2Module = load_brane_modules()

