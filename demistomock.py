# NOTE: This module must be loaded before any Demisto drivers are loaded.

from typing import Optional
from Packs.ApiModules.Scripts.DemistoClassApiModule.DemistoClassApiModule import Demisto

demisto: Optional[Demisto] = None

def setup(context: dict) -> None:
    global demisto
    demisto = Demisto(context)

# We are monkey patching `hasattr`! By creating our own "demistomock.py", we
# will be imported when drivers write "import demistomock as demisto".
#
# https://code.activestate.com/lists/python-list/14972
def _hasattr(obj: object, attr: str, orig_hasattr=hasattr) -> bool:
    if orig_hasattr(obj, '__hasattr__'):
        return obj.__hasattr__(attr) # type: ignore
    return orig_hasattr(obj, attr)
__builtins__['hasattr'] = _hasattr

# When something has `import demistomock as demisto`, and then does something like
# `demisto.xyz`, we will redirect it to the value created in `setup()` above
def __getattr__(attr):
    if demisto is not None:
        return getattr(demisto, attr)

def __setattr__(attr, value):
    if demisto is not None:
        return setattr(demisto, attr, value)

# When something has `import demistomock as demisto`, and then does something like
# `demisto.hasattr(...)`, we will redirect it to the value created in `setup()` above
def __hasattr__(attr):
    if demisto is not None:
        return hasattr(demisto, attr)
