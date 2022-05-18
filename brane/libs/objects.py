from __future__ import annotations
from brane.typing import *
from brane.core.object import Object
from brane.libs.modules import className2Module
from brane.libs.formats import className2Format

class PIL_Image_Object(Object):
    format = className2Format["JPEG"]
    module = className2Module["Pillow"]

    @classmethod
    def load_objects(cls):
        from PIL import Image as PILImage
        cls.object_type = PILImage.Image

class PIL_JPEG_Object(Object):
    format = className2Format["JPEG"]
    module = className2Module["Pillow"]

    @classmethod
    def load_objects(cls):
        from PIL import JpegImagePlugin
        cls.object_type = JpegImagePlugin.JpegImageFile

class PIL_PNG_Object(Object):
    format = className2Format["PNG"]
    module = className2Module["Pillow"]

    @classmethod
    def load_objects(cls):
        from PIL import PngImagePlugin
        cls.object_type = PngImagePlugin.PngImageFile

class Pandas_DataFrame_Object(Object):
    type_evaluation = "isinstance"### temporal name and value
    format_checker = lambda obj: className2Format["CSV"]
    module_checker = lambda obj, fmt: className2Module["Pandas"]

    @classmethod
    def load_objects(cls):
        import pandas as pd
        cls.object_type = pd.DataFrame

class Json_Json_Object(Object):
    format = className2Format["Json"]
    module = className2Module["Json"]

    @classmethod
    def load_objects(cls):
        cls.object_type = dict
