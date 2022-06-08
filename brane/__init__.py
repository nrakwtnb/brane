from brane.core.iomanager import ExtendedIO  # noqa: F401

ExtendedIO.setup_hooks()

import os  # noqa: E402

if os.environ.get("BRANE_MODE", None) == 'debug':
    print("brane.__init__.py called")
