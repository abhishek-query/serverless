import sys
import logging

handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


debug = logger.debug
info  = logger.info
warn  = logger.warn
error = logger.error

__all__ = ['debug', 'info', 'warn', 'error', 'logger']
