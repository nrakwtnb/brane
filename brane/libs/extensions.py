from __future__ import annotations
from brane.typing import *
from brane.core.extension import Extension
from brane.core.utils import generate_classes

def register_Extension_classes(class_info):
    generate_classes(class_info, (Extension,), suffix="Extension")
info = {
    "JPEG": {
        "name": "jpg",
        "variation": ["jpeg"]
    },
    "PNG": {
        "name": "png",
    },
    "CSV": {
        "name": "csv",
    },
    "TSV": {
        "name": "tsv",
    },
    "JSON": {
        "name": "json",
    },
}

# temporal
register_Extension_classes(info)
