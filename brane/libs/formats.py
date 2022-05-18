from __future__ import annotations
from brane.typing import *
class DataType():
    pass

class ImageType():
    pass

class TableType():
    pass

class ArrayType():# List
    pass

class CollectionType():# other data containers
    pass

class DictType():# Map
    pass

class TextType():
    pass
from brane.core.format import Format
from brane.libs.modules import className2Module

class JPEGFormat(Format):
    name = "JPEG"
    data_type = ImageType
    default_extension = "jpg"
    variation = ["jpeg"]
    module = className2Module["Pillow"]

class CSVFormat(Format):
    data_type = TableType
    default_extension = "csv"
    module = className2Module["Pandas"]
#from brane.core.format import create_format_class

# [alternative (class generation from config)]
format_data = {
    "PNG": dict(
        data_type = ImageType,
        default_extension = "png",
        module = className2Module["Pillow"],
    ),
    "Json": dict(
        data_type = DictType,
        default_extension = "json",
        module = className2Module["Json"],
    ),
    "TSV": dict(
        data_type = TableType,
        default_extension = "tsv",
        module = className2Module["Pandas"],
    ),
}

def create_format_class(name: str, default_extension: str, module: ModuleClassType, variation: list[str] = [], data_type=None):
    attributes = dict(
        name = name,
        data_type = data_type,
        default_extension = default_extension,
        module = module,
    )
    #if name is None:
    #    name = default_extension
    return type(f"{name}Format", (Format, ), attributes)

className2Format = {
    "JPEG": JPEGFormat,
    "CSV": CSVFormat,
    **{
        name: create_format_class(name=name, **params)
        for name, params in format_data.items()
    },
}
