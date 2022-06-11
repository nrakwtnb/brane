from __future__ import annotations

from brane.core.factory import BraneClassGenerator
from brane.core.hook import Hook
from brane.typing import *  # noqa: F403


class PILResizeHook(Hook):
    hook_name = "PILResize"

    def __init__(self, size: tuple[int, int], resample=None):
        from PIL import Image as PILImage

        if resample is None:
            resample = PILImage.BILINEAR
        self.size = size
        self.resample = resample

    def condition(self, info: ContextInterface) -> bool:
        obj = info.get("object", None)
        is_jpeg: bool = isinstance(obj, BraneClassGenerator.className2Object["PIL_JPEG"].object)
        is_png: bool = isinstance(obj, BraneClassGenerator.className2Object["PIL_PNG"].object)
        return is_jpeg or is_png

    def __call__(self, info: ContextInterface) -> Any:  # [TODO]: replace Any by the correct type
        print("resize")
        obj = info.get("object")
        return obj.resize(self.size, self.resample)
