# Brane: Extensible data I/O interface with hook systems and data tracking 

Brane is designed to provide a rich I/O management system in the Python programming.
The goals are

* to avoid setting the common arguments or processings on the I/O events
* to be allowed to track data flows

Then, we can save time, get less human error and make codes readable.

## Installation

### Dependencies

Requirements
* PyYAML
* typing-extension (Python 3.7)

You also need other modules for reading or writing depending on use cases.

### Via PyPI

You can use any tools such as pip, pipenv or poetry:

```sh
$ pip install brane
$ pipenv install brane
$ poetry add brane
```

Currently, the conda installation is not supported yet.

### Via Github Source

```sh
$ pip install git+https://github.com/nrakwtnb/brane.git
$ pipenv install git+https://github.com/nrakwtnb/brane.git#egg=brane
```

If you'd like to specify the version, try
```sh
$ pip install git+https://github.com/nrakwtnb/brane.git@<version>#egg=brane
$ pipenv install git+https://github.com/nrakwtnb/brane.git@<version>#egg=brane
```
where the version can be one of
* 0.0dev0

## Document

See [Document](https://nrakwtnb.github.io/brane/).

### Features

### Usage

#### Unified I/O Interface

```python
from brane import ExtendedIO as xio

# read a single file
path: str = "<path to load>"
obj = xio.read(path)

# read multiple files
path_list: list[str] = ["<path1>", "<path2>", ...]
objs = xio.read_all_as_list(path_list)

# write
save_path: str = "<path to save>"
xio.write(obj, save_path)

# write multiple objects
output_dir: str = "<output_dir>"
name2obj = {"<name1>": <obj1>, "<name2>": <obj2>, ...}
xio.write_all_from_dict(name2obj, output_dir=output_dir)
```

#### Hook system

```python
from brane import ExtendedIO as xio

# set a hook of postprocess after loading an object
def postprocess(context):
    obj = context["object"]
    # ... some postprocess on obj
    return processed_obj

def check_condition(context) -> bool:
    obj = context["object"]
    path = context["path"]
    # ... determine whether the hook is called or not
    return called


xio.register_post_read_hook(hook=postprocess, condition_func=check_condition)

# set a hook of optimiation before objects with the certain type are saved
target_obj_type = <object type>
def optimize(context):
    obj = context["object"]
    # ... some optimization process on obj
    return optimized_obj

xio.register_pre_write_hook(hook=optimize, object_type=target_obj_type)
```

### Examples

See [Example Page](examples).

## Information

### License

Apache 2.0

### Changelog

## Development

### Contribution

