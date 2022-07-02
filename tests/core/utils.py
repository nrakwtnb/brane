from brane.core.module import Module
from brane.core.format import Format
from brane.core.object import Object


class TextModule(Module):
    name = "text"

    @classmethod
    def read(cls, path: str, *args, **kwargs):
        with open(path, "r") as f:
            text = f.read()
        return text

    @classmethod
    def write(cls, obj, path, *args, **kwargs):
        with open(path, "w") as f:
            f.write(obj)


class TextFormat(Format):
    name = "text"
    module = TextModule
    default_extension = "text"


class TextObject(Object):
    format = TextFormat
    module = TextModule
    object_type = str
    priority = 100
