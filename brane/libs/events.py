from __future__ import annotations

from brane.core.hook import FunctionHook  # noqa: E402
from brane.libs.hooks import check_path_existence, create_parent_directory  # noqa E402
from brane.typing import *  # noqa: F401, F403

BasicEvents.read_pre.add_hooks(FunctionHook(check_path_existence))
BasicEvents.write_pre.add_hooks(FunctionHook(create_parent_directory))
from brane.libs.hooks import check_path_existence, create_parent_directory  # noqa E402
