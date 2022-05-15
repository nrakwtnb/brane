from __future__ import annotations
from brane.typing import *
from brane.core.object import Object
from brane.libs.modules import PILModule, PandasModule, JsonModule
from brane.libs.formats import JPEGFormat, PNGFormat, CSVFormat, JsonFormat

class PIL_Image_Object(Object):
    format = JPEGFormat
    module = PILModule
    #write = PILModule.write

    @classmethod
    def load_objects(cls):
        from PIL import Image as PILImage
        cls.object_type = PILImage.Image

class PIL_JPEG_Object(Object):
    format = JPEGFormat
    module = PILModule
    #write = PILModule.write

    @classmethod
    def load_objects(cls):
        from PIL import JpegImagePlugin
        cls.object_type = JpegImagePlugin.JpegImageFile

class PIL_PNG_Object(Object):
    format = PNGFormat###
    module = PILModule
    #write = PILModule.write

    @classmethod
    def load_objects(cls):
        from PIL import PngImagePlugin
        cls.object_type = PngImagePlugin.PngImageFile

class Pandas_DataFrame_Object(Object):
    type_evaluation = "isinstance"### temporal name and value
    format_checker = lambda obj: CSVFormat
    module_checker = lambda obj, fmt: PandasModule

    @classmethod
    def load_objects(cls):
        import pandas as pd
        cls.object_type = pd.DataFrame

class Json_Json_Object(Object):
    format = JsonFormat
    module = JsonModule

    @classmethod
    def load_objects(cls):
        cls.object_type = dict
