from __future__ import annotations

from brane.core.event import Event
from brane.typing import *  # noqa: F401, F403


class BasicEvents(object):
    read_pre = Event(event_name="read_pre")
    read_post = Event(event_name="read_post")
    write_pre = Event(event_name="write_pre")
    write_post = Event(event_name="write_post")

    readall_pre = Event(event_name="readall_pre")
    readall_post = Event(event_name="readall_post")
    writeall_pre = Event(event_name="writeall_pre")
    writeall_post = Event(event_name="writeall_post")


from brane.core.hook import FunctionHook  # noqa: E402
from brane.libs.hooks import check_path_existence, create_parent_directory  # noqa E402

BasicEvents.read_pre.add_hooks(FunctionHook(check_path_existence))
BasicEvents.write_pre.add_hooks(FunctionHook(create_parent_directory))
