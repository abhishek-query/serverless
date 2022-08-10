# NOTE: This module must be loaded before any Demisto drivers are loaded.
#
# Demisto drivers typically have
#
#   import demistomock as demisto
#
# and they interact with this demisto module as if it was the Demisto class, even though it is
# some kind of test module.
#
# Our module will be loaded instead. We've subclassed `Demisto` to override the interface it
# provides between the Python driver and some kind of server which reads commands from STDIN and
# prints the results to STDOUT.
#
# We maintain a single instance of this class and forward all calls to that instance. Beware
# that having this single instance is essentially like having a global variable.

import logging
from typing import Optional
from queryai.demisto import Demisto
from queryai.logging import logger

__all__ = ['__hasattr__', '__getattr__', '__setattr__']

_demisto: Optional[Demisto] = None

def setup(context: dict) -> None:
    global _demisto
    _demisto = Demisto(context)

# When something has `import demistomock as demisto`, and then does something like
# `demisto.xyz`, we will redirect it to the value created in `setup()` above
def __getattr__(attr):
    if _demisto is not None:
        return getattr(_demisto, attr)

def __setattr__(attr, value):
    logger.debug(f'demistomock.__setattr__({attr}, {value}')
    if _demisto is not None:
        return setattr(_demisto, attr, value)

def _hasattr(obj: object, attr: str, orig_hasattr=hasattr) -> bool:
    if orig_hasattr(obj, '__hasattr__'):
        return obj.__hasattr__(attr) # type: ignore
    return orig_hasattr(obj, attr)

# We are monkey patching `hasattr`! By creating our own "demistomock.py", we
# will be imported when drivers write "import demistomock as demisto".
#
# https://code.activestate.com/lists/python-list/14972
__builtins__['hasattr'] = _hasattr

# When something has `import demistomock as demisto`, and then does something like
# `demisto.hasattr(...)`, we will redirect it to the value created in `setup()` above
def __hasattr__(attr):
    logger.debug(f'demistomock.__hasattr__({attr})')
    if _demisto is not None:
        return hasattr(_demisto, attr)
