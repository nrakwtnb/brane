from __future__ import annotations

from brane.core.factory import Factory
from brane.core.hook import Hook
from brane.typing import *  # noqa: F403


class PILResizeHook(Hook):
    hook_name = "PILResize"

    def __init__(self, size, resample=None):
        from PIL import Image as PILImage

        if resample is None:
            resample = PILImage.BILINEAR
        self.size = size
        self.resample = resample

    def condition(self, info: ContextInterface):
        obj = info.get("object", None)
        # return isinstance(obj, PIL_JPEG_Object.object) or isinstance(obj, PIL_PNG_Object.object)
        return isinstance(
            obj, Factory.className2Object["PIL_JPEG"].object
        ) or isinstance(obj, Factory.className2Object["PIL_PNG"].object)

    def __call__(self, info: ContextInterface):
        print("resize")
        obj = info.get("object")
        return obj.resize(self.size, self.resample)


import os  # noqa: E402


# add candidate suggestion function ?
def check_path_existence(info):
    path = info["path"]
    assert os.path.exists(path), f"The specified path is not found, {path}"


def create_parent_directory(info):
    path = info["path"]
    parent_dir = os.path.dirname(path)
    os.makedirs(parent_dir, exist_ok=True)
