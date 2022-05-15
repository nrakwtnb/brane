from __future__ import annotations
from brane.typing import *
from brane.core.module import Module
# temproal (Module ? Enccoding/Decoding ?)

class PILModule(Module):
    name = "PIL"### pillow ?
    object_method_write = "save"

    @classmethod
    def load_modules(cls):
        from PIL import Image as PILImage
        cls.module = PILImage
        cls.module_method_read = PILImage.open

class CV2Module(Module):
    name = "cv2"
    
    @classmethod
    def load_modules(cls):
        import cv2
        cls.module = cv2
        cls.module_method_read = cv2.imread
        cls.module_method_write = cv2.imwrite
        swap_args = True

class PandasModule(Module):
    name = "pandas"
    base_kwargs_write = {"index":None}
    object_method_write = "to_csv"

    @classmethod
    def load_modules(cls):
        import pandas as pd
        cls.module = pd
        cls.module_method_read = pd.read_csv

class JsonModule(Module):
    name = "json"
    base_kwargs_write = {"indent":2}

    @classmethod
    def load_modules(cls):
        import json
        cls.module = json

    @classmethod
    def read(cls, file, *args, **kwargs):
        import json
        with open(file, "r") as f:
            obj = json.load(fp=f, *args, **kwargs)
        return obj

    @classmethod
    def write(cls, obj, file, *args, **kwargs):
        import json
        with open(file, "w") as f:
            json.dump(obj=obj, fp=f, *args, **kwargs)
        return True###

class TextIOModule(Module):
    name = "textio"###
    loaded = True

    #@classmethod
    #def load_modules(cls):
    #    pass

    @classmethod
    def read(cls, file, *args, **kwargs):
        with open(file, "r") as f:
            text = f.readlines(*args, **kwargs)
        return text

    @classmethod
    def write(cls, obj, file, *args, **kwargs):
        with open(file, "w") as f:
            f.writelines(text, *args, **kwargs)
        return True###
