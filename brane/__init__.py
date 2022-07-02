__version__ = "v0.0.dev1"

import os  # noqa: E402

if 'debug' in os.environ.get("BRANE_MODE", ""):
    print("brane.__init__.py called")
if 'noninit' not in os.environ.get("BRANE_MODE", ""):
    from brane.core.xio import ExtendedIO  # noqa: F401

    ExtendedIO.setup_hooks()
