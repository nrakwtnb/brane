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
from brane.libs.modules import PILModule, PandasModule, JsonModule

# temporal (Data ? Format ?)
class JPEGFormat(Format):
    data_type = ImageType
    default_extension = "jpg"
    #module_read = PILImage
    #module_write = PILImage
    #read = PILModule.read### exp
    module = PILModule### exp

#class PNGFormat(Format):
#    data_type = ImageType
#    default_extension = "png"
#    read = PILModule.read### exp

class TSVFormat(Format):
    data_type = TableType
    default_extension = "tsv"
    #read = PandasModule.read### exp
    module = PandasModule### exp

class CSVFormat(Format):
    data_type = TableType
    default_extension = "csv"
    #read = PandasModule.read### exp
    module = PandasModule### exp
attributes = dict(
    data_type = ImageType,
    default_extension = "png",
    #read = PILModule.read### exp
    module = PILModule### exp
)
PNGFormat = type("PNGFormat", (Format, ), attributes)

attributes = dict(
    data_type = DictType,
    default_extension = "json",
    #read = PILModule.read### exp
    module = JsonModule### exp
)
JsonFormat = type("JsonFormat", (Format, ), attributes)
