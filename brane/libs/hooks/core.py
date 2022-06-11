from __future__ import annotations

import os  # noqa: E402

from brane.typing import *  # noqa: F403


# add candidate suggestion function ?
def check_path_existence(info: ContextInterface):
    path = info["path"]
    assert os.path.exists(str(path)), f"The specified path is not found, {path}"


def create_parent_directory(info: ContextInterface):
    path = info["path"]
    parent_dir = os.path.dirname(str(path))
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
