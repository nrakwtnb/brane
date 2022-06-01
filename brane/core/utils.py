from __future__ import annotations
from brane.typing import *

def integrate_args(base_args: tuple, new_args: tuple) -> tuple:
    if len(base_args) >= len(new_args):
        base_args_list = list(base_args)
    else:
        additional_num = len(new_args) - len(base_args)
        base_args_list = list(base_args) + \
            [None for _ in range(additional_num)]

    for i, arg in enumerate(new_args):
        if arg is not None:
            base_args_list[i] = arg
    return tuple(base_args_list)


def integrate_kwargs(base_kwargs: dict, new_kwargs: dict) -> dict:
    return {**base_kwargs, **new_kwargs}

def generate_classes(info_dict: dict, bases=(object,), prefix: str = "", suffix: str = ""):  # temporal name
    info = info_dict.copy()
    generated_classes_info = {}

    for class_name, class_info in info.items():
        full_class_name = prefix+class_name+suffix
        _ = type(full_class_name, bases, class_info)
import os


def get_extension_from_filname_default(path: str) -> str:
    ext = os.path.splitext(path)[1][1:]
    return ext
